'''
Inject TagWorks result annotations into the original TEI document. 
Also produce intermediary csv annotations in the same csv format as the original softcite dataset

The process is as follow:
- read the TagWorks csv result file
- read the text and map file to synchronize back to the TEI/JSON, similar as we know the JSON chunks reflect exactly the TEI text flow
- inject inline tags in similar format as for the original corpus

Input result TagWokrs format is the "cleaned-up" one, as follow:

article_batch_name,article_filename,mention_id,taskrun_count,taskrun_id,answer_label,answer_text,case_number,highlight_count,start_pos,end_pos,target_text

For the TEI injection, in case we have multiple contradicting annotations:
- we log the non-agreement
- as first default method, we take the first annotation

-> TBD: define some methodology for contradicting annotations and reconciliation

'''

import os
import json
import csv
import argparse
import gzip
from lxml import etree
import lxml.html
from collections import OrderedDict
from xml.sax import saxutils


fields = ["software", "version", "url", "publisher", "used"]
p_indent = "            "

def enrich_tei_files_via_json(tagworks_file, json_corpus_path, output_path, collection=None):
    # the following will not work on windows...
    base_tagworks_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(tagworks_file)))))
    document_ids, documents = _parse_tagworks_result_cvs(tagworks_file, base_tagworks_dir)
    documents = _resolve_conflicting_annotations(documents)

    # init the TEI corpus file for the tagworks snippets and labels - we use mustache style templates
    with open('resources/corpus.template.tei.xml', mode='r') as f:
        corpus_template = f.read()

    # init the doc level template    
    with open('resources/document-element.tei.xml', mode='r') as f:
        doc_template = f.read()

    # go through the documents
    doc_tei = []
    for doc_id in document_ids:
        print("processing", doc_id)
        document = documents[doc_id]
        #print(document)

        if 'annotations' not in document:
            continue

        # python string are immutable...
        local_doc_template = doc_template
        local_doc_template = local_doc_template.replace("{{ORIGIN}}", doc_id)

        if collection is None:
            local_doc_template = local_doc_template.replace("{{COLLECTION}}", "")
        else:
            local_doc_template = local_doc_template.replace("{{COLLECTION}}", 'subtype="'+collection+'" ')

        paragraph_ranks = []
        section_ranks = []
        for the_file_path in document["file_paths"]:
            map_file_path = os.path.join(base_tagworks_dir,the_file_path.replace('text.txt.gz','map.csv.gz'))
            #print(map_file_path)
            with gzip.open(map_file_path, mode='rt') as csv_file:
                # map is pretty complex, we are interested in local and global offsets
                # file_path,article,entity_json_start,entity_json_end,entity_type,entity_rawForm,entity_resp,entity_used,entity_id,entity_cert,entity_start_in_chunk,entity_end_in_chunk,entity_start_in_text,entity_end_in_text,entity_count_val,text,text_num,text_modify,text_chr_count,text_end_chr,text_start_chr,chunk_offset_end,chunk_offset_start,chunk_length,chunk_entity_count,orig_text,section_rank,paragraph_rank,is_section_title,max_text_in_paragraph,is_paragraph_end,num_in_chunk,test_entity_rawForm_by_offset_chunk,test_entity_rawForm_by_offset_text,selected_by_mention,chunk_selected_by     
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row['paragraph_rank'] == 'NA':
                        continue
                    paragraph_rank = row['paragraph_rank']
                    section_rank = row['section_rank']
                    if paragraph_rank not in paragraph_ranks:
                        paragraph_ranks.append(paragraph_rank)
                    if section_rank not in section_ranks:
                        section_ranks.append(section_rank)

        #print(paragraph_ranks)
        #print(section_ranks)

        # access and parse the corresponding JSON document
        json_file = os.path.join(json_corpus_path, doc_id+".json")
        print("json file:", json_file)
        with open(json_file, "r") as the_json_file:
            json_doc = json.load(the_json_file, object_pairs_hook=OrderedDict)

        # get snippets sections
        paragraphs = []
        _abstract = json_doc['abstract']
        body_text = json_doc['body_text']

        for element in _abstract:
            if "paragraph_rank" not in element:
                continue
            if "paragraph_rank" in element:
                if str(element['paragraph_rank']) in paragraph_ranks:
                    paragraphs.append(element)
        for element in body_text:
            if "paragraph_rank" not in element:
                continue
            if "paragraph_rank" in element:
                if str(element['paragraph_rank']) in paragraph_ranks:
                    paragraphs.append(element)

        all_p_tei = []

        #print(paragraphs)
        for element in paragraphs:
            p_tei = element['text']
            p_tei_length = len(p_tei)

            markups = []

            # serialize in XML 
            # first reference markers
            if "ref_spans" in element:
                for span in element['ref_spans']:
                    start = int(span["start"])
                    end = int(span["end"])

                    attributes = []
                    attributes.append(["type", span['type']])
                    markup = _create_markup(start, "ref", attributes)
                    markups.append(markup)

                    markup2 = _create_markup(end, "/ref")
                    markups.append(markup2)

            # then tagworks spans (log warning and discard it when overlapping a reference marker)
            mentions_done = []
            for mention_id in document['annotations']:
                if mention_id in mentions_done:
                    continue
                mention_consumed = False
                software_pos = -1
                local_annotations = document['annotations'][mention_id]
                for annotation in local_annotations:
                    field = annotation['field']
                    if field == 'used':
                        continue

                    # determine the offset shift of the paragraph with respect to the task "snippet"
                    snippet = None
                    paragraph_pos = -1
                    if 'context' in annotation:
                        snippet = annotation['context']

                        paragraph_pos = snippet.find(p_tei)
                        if paragraph_pos == -1:
                            # there are two cases to consider here:
                            # 1) first paragraph is cut, we need to match the first partial paragraph in the snippet text,
                            #    ajusted offset will be position of the cut
                            # 2) last paragraph is cut, we need to match the last partial paragraph in the snippet text,
                            #    ajusted offset will be the start of this cut paragraph in the snippet text
                            snippet_first = _get_first_paragraph(snippet)
                            start_pos = p_tei.find(snippet_first)
                            if start_pos != -1:
                                paragraph_pos = - start_pos
                            else:
                                snippet_last, pos_last = _get_last_paragraph(snippet)
                                if p_tei.find(snippet_last) != -1:
                                    paragraph_pos = pos_last

                            if paragraph_pos == -1:        
                                print("Error:", "the paragraph is not found in the task snippet!", p_tei, annotation["file_path"])                    
                    
                    start = -1
                    end = -1
                    if paragraph_pos != -1:                            
                        if "start" in annotation:
                            start = annotation["start"] - paragraph_pos
                        if "end" in annotation:
                            end = annotation["end"] - paragraph_pos
                        if start > p_tei_length or end > p_tei_length or start < 0 or end < 0:
                            continue
                        # check that the span and the annotation text are matching
                        if annotation['text'] != p_tei[start:end]:
                            continue
                    else:
                        #continue
                        # otherwise we try direct match, with a control of software name position in case of software attributes
                        ind = p_tei.find(annotation['text'])
                        if ind != -1:
                            local_matches = [ind]
                            # more matches?
                            ind2 = ind
                            while ind2 != -1:
                                ind2 = p_tei.find(annotation['text'], ind2+1)
                                if ind2 != -1:
                                    local_matches.append(ind2)
                            if len(local_matches) == 1 and annotation['field'] == 'software':
                                start = ind
                                end = start + len(annotation['text'])
                            elif annotation['field'] != 'software':
                                # select a match after software name position
                                if software_pos != -1:
                                    for local_pos in local_matches:
                                        if local_pos > software_pos:
                                            start = local_pos
                                            end = start + len(annotation['text'])
                                            break
                    if start == -1 or end == -1:
                        continue
                    
                    mention_id = annotation['mention_id']

                    attributes = []
                    attributes.append(["type", field])
                    if field == 'software':
                        attributes.append(["xml:id", mention_id])
                        is_used = _check_is_used(local_annotations)
                        if is_used:
                            attributes.append(["subtype", "used"])
                        software_pos = start
                    else:
                        attributes.append(["corresp", '#'+mention_id])
                    markup = _create_markup(start, "rs", attributes)
                    markups.append(markup)

                    markup2 = _create_markup(end, "/rs")
                    markups.append(markup2)

                    mention_consumed = True

                if mention_consumed:
                    mentions_done.append(mention_id)

            for mention_id in mentions_done:
                del document['annotations'][mention_id]

            # sort the markups by position (bubble sort)
            for iter_num in range(len(markups)-1,0,-1):
                for idx in range(iter_num):
                    if markups[idx]['pos']>markups[idx+1]['pos']:
                        temp = markups[idx]
                        markups[idx] = markups[idx+1]
                        markups[idx+1] = temp

            i = len(markups)-1
            while i>=0:
                markup = markups[i]
                pos = markup['pos']
                # we use placeholders for xml special characters to ensure correct XML text encoding
                new_p_tei = p_tei[:pos]+'𐎨'+markup['tag']
                if 'attributes' in markup:
                    attributes = markup['attributes']
                    for attribute in attributes:
                        new_p_tei += ' ' + attribute[0]+'="'+attribute[1]+'"'
                new_p_tei +='𐎩'+p_tei[pos:]
                p_tei = new_p_tei
                i -= 1    

            p_tei = saxutils.escape(p_tei)
            # restore placeholders
            p_tei = p_tei.replace("𐎨", "<")
            p_tei = p_tei.replace("𐎩", ">")
            p_tei = p_indent+"<p>"+p_tei+"</p>"
            all_p_tei.append(p_tei)

        paragraph_tei_sequence = ''
        for element_tei in all_p_tei:
            paragraph_tei_sequence += element_tei + '\n'
        local_doc_template = local_doc_template.replace("{{PARAGRAPH}}", paragraph_tei_sequence)

        doc_tei.append(local_doc_template)

    doc_tei_sequence = ''
    for element_tei in doc_tei:
        doc_tei_sequence += element_tei + '\n'

    corpus_template = corpus_template.replace('{{TEI_ENTRIES}}', doc_tei_sequence)

    # save the TEI corpus file
    with open(os.path.join(output_path, "softcite_corpus_tagworks.tei.xml"), "w") as out_file:
        out_file.write(corpus_template)

def enrich_tei_files_via_tei_corpus(tagworks_file, tei_corpus_path, output_path, collection=None):
    # the following will not work on windows...
    base_tagworks_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(tagworks_file)))))
    document_ids, documents = _parse_tagworks_result_cvs(tagworks_file, base_tagworks_dir)
    documents = _resolve_conflicting_annotations(documents)

    # init the TEI corpus file for the tagworks snippets and labels - we use mustache style templates
    with open('resources/corpus.template.tei.xml', mode='r') as f:
        corpus_template = f.read()

    # init the doc level template    
    with open('resources/document-element.tei.xml', mode='r') as f:
        doc_template = f.read()

    # read the id mapping file associated to the TEI Corpus file
    base_tei_dir = os.path.dirname(os.path.realpath(tei_corpus_path))
    # used to map SoftCite corpus id and document identifiers (DOI, PMCID, PMID)
    identifiers = read_id_map(os.path.join(base_tei_dir, "ids.csv"))

    # read the existing TEI corpus file
    parser = etree.XMLParser(remove_blank_text=False)
    root_corpus = etree.parse(tei_corpus_path, parser).getroot()

    # go through the documents
    doc_tei = []
    for doc_id in document_ids:
        print("processing", doc_id)
        document = documents[doc_id]
        #print(document)

        if 'annotations' not in document:
            continue

        # python string are immutable...
        local_doc_template = doc_template
        local_doc_template = local_doc_template.replace("{{ORIGIN}}", doc_id)

        if collection is None:
            local_doc_template = local_doc_template.replace("{{COLLECTION}}", "")
        else:
            local_doc_template = local_doc_template.replace("{{COLLECTION}}", 'subtype="'+collection+'" ')

        '''
        paragraph_ranks = []
        section_ranks = []
        for the_file_path in document["file_paths"]:
            map_file_path = os.path.join(base_tagworks_dir,the_file_path.replace('text.txt.gz','map.csv.gz'))
            #print(map_file_path)
            with gzip.open(map_file_path, mode='rt') as csv_file:
                # map is pretty complex, we are interested in local and global offsets
                # file_path,article,entity_json_start,entity_json_end,entity_type,entity_rawForm,entity_resp,entity_used,entity_id,entity_cert,entity_start_in_chunk,entity_end_in_chunk,entity_start_in_text,entity_end_in_text,entity_count_val,text,text_num,text_modify,text_chr_count,text_end_chr,text_start_chr,chunk_offset_end,chunk_offset_start,chunk_length,chunk_entity_count,orig_text,section_rank,paragraph_rank,is_section_title,max_text_in_paragraph,is_paragraph_end,num_in_chunk,test_entity_rawForm_by_offset_chunk,test_entity_rawForm_by_offset_text,selected_by_mention,chunk_selected_by     
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if row['paragraph_rank'] == 'NA':
                        continue
                    paragraph_rank = row['paragraph_rank']
                    section_rank = row['section_rank']
                    if paragraph_rank not in paragraph_ranks:
                        paragraph_ranks.append(paragraph_rank)
                    if section_rank not in section_ranks:
                        section_ranks.append(section_rank)
        '''
        #print(paragraph_ranks)
        #print(section_ranks)

        # access the corresponding TEI entry in the TEI corpus document
        softcite_doc_id = identifiers[doc_id]
        if softcite_doc_id is None:
            print("ERROR: the SoftCite unique doc id cannot be retrieved from TagWorks file doc identifier:", doc_id)
            continue

        local_doc_template = local_doc_template.replace("{{DOCUMENT_UID}}", softcite_doc_id)

        expression = "//tei:TEI[descendant::tei:fileDesc[@xml:id='"+softcite_doc_id+"']]/tei:text/tei:body/tei:p"
        paragraphs = root_corpus.xpath(expression, namespaces={'tei': 'http://www.tei-c.org/ns/1.0'})
        #print("found", str(len(paragraphs)), "paragraphs for", softcite_doc_id)
        
        all_p_tei = []

        #print(paragraphs)
        for element in paragraphs:
            markups = []

            # set reference markers
            current_pos = 0
            for elem in element.getiterator():
                if elem.attrib.items():
                    for key, value in elem.attrib.items():
                        if key == 'type':
                            the_type = value

                    attributes = []
                    attributes.append(["type", the_type])
                    if elem.tag is not None and elem.tag.endswith('ref'):
                        markup = _create_markup(current_pos, "ref", attributes)
                        markups.append(markup)
                if elem.text:
                    current_pos += len((elem.text))

                if elem.tail:
                    if elem.tag is not None and elem.tag.endswith('ref'):
                        markup2 = _create_markup(current_pos, "/ref")
                        markups.append(markup2)
                    #print("current pos:", current_pos)
                    #print('my tail:', elem.tail, "|")
                    # for some unknown reasons, the lxml parser insert spurious indentation here
                    if elem.tail.find("\n") == -1 and elem.tail.find("\t") == -1:
                        current_pos += len((elem.tail))
            
            etree.strip_tags(element,'*')
            p_tei = element.text
            p_tei_length = len(p_tei)
            #print(p_tei)

            # then tagworks spans (log warning and discard it when overlapping a reference marker)
            mentions_done = []
            for mention_id in document['annotations']:
                if mention_id in mentions_done:
                    continue
                mention_consumed = False
                software_pos = -1
                local_annotations = document['annotations'][mention_id]
                for annotation in local_annotations:
                    field = annotation['field']
                    if field == 'used':
                        continue

                    # determine the offset shift of the paragraph with respect to the task "snippet"
                    snippet = None
                    paragraph_pos = -1
                    if 'context' in annotation:
                        snippet = annotation['context']

                        paragraph_pos = snippet.find(p_tei)
                        if paragraph_pos == -1:
                            # there are two cases to consider here:
                            # 1) first paragraph is cut, we need to match the first partial paragraph in the snippet text,
                            #    ajusted offset will be position of the cut
                            # 2) last paragraph is cut, we need to match the last partial paragraph in the snippet text,
                            #    ajusted offset will be the start of this cut paragraph in the snippet text
                            snippet_first = _get_first_paragraph(snippet)
                            start_pos = p_tei.find(snippet_first)
                            if start_pos != -1:
                                #paragraph_pos = - start_pos
                                paragraph_pos = 0
                                # we remove the starting part of p_tei not in the snippet
                                p_tei = p_tei[start_pos:]
                                # existing bib ref has to be shifted :/
                                for markup in markups:
                                    markup['pos'] = markup['pos'] - start_pos
                            else:
                                snippet_last, pos_last = _get_last_paragraph(snippet)
                                if p_tei.find(snippet_last) != -1:
                                    paragraph_pos = pos_last
                                    # we remove the tail part of p_tei not present in the snippet
                                    p_tei = p_tei[:len(snippet_last)]

                            if paragraph_pos == -1:        
                                print("Error:", "the paragraph is not found in the task snippet!", p_tei, annotation["file_path"])                    
                    
                    start = -1
                    end = -1
                    if paragraph_pos != -1:                            
                        if "start" in annotation:
                            start = annotation["start"] - paragraph_pos
                        if "end" in annotation:
                            end = annotation["end"] - paragraph_pos
                        if start > p_tei_length or end > p_tei_length or start < 0 or end < 0:
                            continue
                        # check that the span and the annotation text are matching
                        if annotation['text'] != p_tei[start:end]:
                            continue
                    else:
                        #continue
                        # otherwise we try direct match, with a control of software name position in case of software attributes
                        ind = p_tei.find(annotation['text'])
                        if ind != -1:
                            local_matches = [ind]
                            # more matches?
                            ind2 = ind
                            while ind2 != -1:
                                ind2 = p_tei.find(annotation['text'], ind2+1)
                                if ind2 != -1:
                                    local_matches.append(ind2)
                            if len(local_matches) == 1 and annotation['field'] == 'software':
                                start = ind
                                end = start + len(annotation['text'])
                            elif annotation['field'] != 'software':
                                # select a match after software name position
                                if software_pos != -1:
                                    for local_pos in local_matches:
                                        if local_pos > software_pos:
                                            start = local_pos
                                            end = start + len(annotation['text'])
                                            break
                        
                    if start == -1 or end == -1:
                        continue
                    
                    mention_id = annotation['mention_id']

                    attributes = []
                    attributes.append(["type", field])
                    if field == 'software':
                        attributes.append(["xml:id", mention_id])
                        is_used = _check_is_used(local_annotations)
                        if is_used:
                            attributes.append(["subtype", "used"])
                        software_pos = start
                    else:
                        attributes.append(["corresp", '#'+mention_id])
                    markup = _create_markup(start, "rs", attributes)
                    markups.append(markup)

                    markup2 = _create_markup(end, "/rs")
                    markups.append(markup2)

                    mention_consumed = True

                if mention_consumed:
                    mentions_done.append(mention_id)

            if len(mentions_done) == 0:
                # no software mention in this paragraph, we can skip it
                continue

            for mention_id in mentions_done:
                del document['annotations'][mention_id]

            # sort the markups by position (bubble sort)
            for iter_num in range(len(markups)-1,0,-1):
                for idx in range(iter_num):
                    if markups[idx]['pos']>markups[idx+1]['pos']:
                        temp = markups[idx]
                        markups[idx] = markups[idx+1]
                        markups[idx+1] = temp

            i = len(markups)-1
            while i>=0:
                markup = markups[i]
                pos = markup['pos']
                if pos < 0:
                    # happen for truncated first paragraph of snippet
                    i -= 1  
                    continue
                if pos > len(p_tei):
                    # happen for truncated last paragraph of snippet
                    i -= 1  
                    continue
                # we use placeholders for xml special characters to ensure correct XML text encoding
                new_p_tei = p_tei[:pos]+'𐎨'+markup['tag']
                if 'attributes' in markup:
                    attributes = markup['attributes']
                    for attribute in attributes:
                        new_p_tei += ' ' + attribute[0]+'="'+attribute[1]+'"'
                new_p_tei +='𐎩'+p_tei[pos:]
                p_tei = new_p_tei
                i -= 1    

            p_tei = saxutils.escape(p_tei)
            # restore placeholders
            p_tei = p_tei.replace("𐎨", "<")
            p_tei = p_tei.replace("𐎩", ">")
            p_tei = p_indent+"<p>"+p_tei+"</p>"
            all_p_tei.append(p_tei)

        if len(all_p_tei) == 0:
            # we did not manage to get annotated paragraphs
            continue

        paragraph_tei_sequence = ''
        for element_tei in all_p_tei:
            paragraph_tei_sequence += element_tei + '\n'
        local_doc_template = local_doc_template.replace("{{PARAGRAPH}}", paragraph_tei_sequence)

        doc_tei.append(local_doc_template)

    doc_tei_sequence = ''
    for element_tei in doc_tei:
        doc_tei_sequence += element_tei + '\n'

    corpus_template = corpus_template.replace('{{TEI_ENTRIES}}', doc_tei_sequence)

    # save the TEI corpus file
    with open(os.path.join(output_path, "softcite_corpus_tagworks.tei.xml"), "w") as out_file:
        out_file.write(corpus_template)



def _get_first_paragraph(snippet):
    end_pos = snippet.find('\n\n')
    par = snippet[:end_pos]
    return par

def _get_last_paragraph(snippet):
    start_pos = snippet.rfind('\n\n')
    par = snippet[start_pos+2:]
    return par, start_pos+2

def _create_markup(position, tag, attributes=None):
    markup = {}
    markup["pos"] = position
    markup["tag"] = tag
    if attributes is not None:
        markup["attributes"] = attributes
    return markup

def _parse_tagworks_result_cvs(tagworks_file, base_tagworks_dir):
    document_ids = []
    documents = {}
    nb_annotations = 0

    # first pass, read the tagworks csv file and build corresponding dict
    # article_batch_name,article_filename,mention_id,taskrun_count,taskrun_id,answer_label,answer_text,case_number,highlight_count,start_pos,end_pos,target_text
    # note: missing annotator uuid, a unique article id would be nice too at this stage (using file name is error-prone)
    with open(tagworks_file, mode='r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            article_id = row['article_filename']
            # postfix with dash must be removed to get the actual file name
            pos = article_id.rfind("-")
            article_id = article_id[:pos]
            if article_id not in document_ids:
                document_ids.append(article_id)
                document_info = {}
                document_info["id"] = article_id
                document_info["file_paths"] = []
            else:
                document_info = documents[article_id]

            if row['answer_label'] in fields:
                annotation = {}
                annotation['field'] = row['answer_label']
                mention_id = row['mention_id']
                taskrun_id = row['taskrun_id']
                annotation['mention_id'] = mention_id
                annotation['taskrun_id'] = taskrun_id

                if row['answer_text'] == 'FALSE':
                    continue

                if annotation['field'] == 'used':
                    if row['answer_text'] == '5' or row['answer_text'] == '4':
                        annotation['value'] = True;
                    else:
                        annotation['value'] = False;
                else:
                    annotation['start'] = int(row['start_pos'])
                    annotation['end'] = int(row['end_pos'])
                    annotation['text'] = row['target_text']
                    nb_annotations += 1
                
                # file path is currently slightly incorrect, the "step1_txt/" is missing
                the_file_path = row['article_batch_name'].replace("/from_json", "/step1_txt/from_json")
                annotation["file_path"] = the_file_path

                # set the text directly to the annotation - this is inefficient but we are dealing with a limited volume anyway 
                # read the txt file corresponding to the case
                if annotation['field'] != 'used':
                    text_file_path = os.path.join(base_tagworks_dir, annotation["file_path"])
                    #print(text_file_path)
                    with gzip.open(text_file_path, 'rt') as f:
                        snippet_text = f.read()
                    annotation['context'] = snippet_text

                if the_file_path not in document_info["file_paths"]:
                    document_info["file_paths"].append(the_file_path)

                if 'annotations' not in document_info:
                    document_info['annotations'] = {}
                if mention_id not in document_info['annotations']:
                    document_info['annotations'][mention_id] = []
                # we want the software always first, it makes thing easier to control
                if annotation['field'] == 'software':
                    document_info['annotations'][mention_id].insert(0, annotation)
                else:
                    document_info['annotations'][mention_id].append(annotation)

            documents[article_id] = document_info

    print("total of", str(len(document_ids)), "documents and ", nb_annotations, "annotations")

    return document_ids, documents

def _get_all_positions(annotations):
    '''
    return spans for all given annotations
    '''
    positions = []
    for annotation in annotations:
        #print(annotation)
        start = -1
        end = -1
        if "start" in annotation:
            start = annotation['start']
        if "end" in annotation:
            end = annotation['end']
        if start != -1 and end != -1:
            pos = {}
            pos['start'] = start
            pos['end'] = end
            positions.append(pos)
    return positions

def _overlap2(pos_set1, pos_set2):
    '''
    return true if two set of spans are overlapping
    '''
    overlap = False
    for position1 in pos_set1:
        for position2 in pos_set1:
            if position1['end'] < position2['start'] or position1['start'] > position2['end']:
                continue
            elif (position1['start'] <= position2['start'] and position1['end'] <= position2['end']) or (position1['start'] >= position2['start'] and position1['end'] >= position2['end']):
                overlap = True;
                break
    return overlap

def _check_is_used(annotations):
    '''
    return true if the annotations contain a positive "used"
    '''
    for annotation in annotations:
        if annotation["field"] == "used":
            return annotation['value']
    return False

def _overlap(pos_set1, pos_set2):
    overlap = False
    for position1 in pos_set1:
        for position2 in pos_set2:
            x = range(position1['start'],position1['end'])
            y = range(position2['start'],position2['end'])
            xs = set(x)
            intersec = xs.intersection(y)
            if len(intersec) != 0:
                overlap = True;
                break
    return overlap

def _get_first_taskrun_id(annotations):
    for annotation in annotations:
        if 'taskrun_id' in annotation:
            return annotation['taskrun_id']
    return None

def _remove_annotation_per_taskrun_id(annotations, taskrun_id):
    '''
    remove annotations not having the given taskrun_id
    '''
    new_annotations = []
    for annotation in annotations:
        if 'taskrun_id' in annotation:
            if annotation['taskrun_id'] == taskrun_id:
                new_annotations.append(annotation)
    return new_annotations

def _resolve_conflicting_annotations(documents):
    '''
    As we have at least 2 annotators per task, we will have conflicting annotations.
    Basically, when two annotations are similar or overlapping, we need to discard one of them.
    '''
    for doc_id in documents:
        document = documents[doc_id]
        if 'annotations' not in document:
            continue

        annotations = document['annotations']
        
        # the list of mention id to be removed
        to_be_removed = []

        for mention_id in annotations:
            if mention_id in to_be_removed:
                continue
            local_annotations = annotations[mention_id]

            # first if we have several taskrun_id for the same mention, we keep only the first one
            taskrun_id = _get_first_taskrun_id(local_annotations)
            if taskrun_id is not None:
                local_annotations_reduced = _remove_annotation_per_taskrun_id(local_annotations, taskrun_id)

                # update local_annotations
                annotations[mention_id] = local_annotations_reduced
                local_annotations = local_annotations_reduced

            all_local_pos = _get_all_positions(local_annotations)                

            # check other annotations
            for mention_id2 in annotations:
                if mention_id == mention_id2:
                    continue
                if mention_id2 in to_be_removed:
                    continue
                local_annotations2 = annotations[mention_id2]
                all_local_pos2 = _get_all_positions(local_annotations2)     
                if _overlap(all_local_pos, all_local_pos2):
                    to_be_removed.append(mention_id2)

        for mention_id in to_be_removed:
            del annotations[mention_id]

        document['annotations'] = annotations

    return documents

def read_id_map(ids_file):
    identifiers = {}
    with open(ids_file, 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            identifiers[row['DOI']] = row['id']
            identifiers[row['origin']] = row['id']
            identifiers[row["PMCID"]] = row['id']
            identifiers[row["PMID"]] = row['id']
            identifiers[row["id"]] = row['origin']
    return identifiers

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Convert a TEI XML file into CORD-19-style JSON format")
    parser.add_argument("--tagworks-file", type=str, help="path to the TagWorks result CSV file (cleanup-up version)")
    parser.add_argument("--json-corpus", type=str, help="path to the directory of full text JSON files from which the tasks have been extracted")
    parser.add_argument("--xml-corpus", type=str, help="path to the SoftCite corpus TEI XML file from which the tasks have been extracted")
    parser.add_argument("--output", type=str, 
        help="path to an output directory where to write the TEI XML file augmented with the TagWorks annotations")

    args = parser.parse_args()
    tagworks_file = args.tagworks_file
    json_corpus_path = args.json_corpus
    tei_corpus_path = args.xml_corpus
    output_path = args.output

    if tagworks_file is None or (json_corpus_path is None and tei_corpus_path is None):
        print("Invalid usage, check expected parameters with --help")
        exit()

    # check path and call methods
    if tagworks_file is not None and not os.path.isfile(tagworks_file):
        print("the path to the TagWorks CSV file is not valid: ", tagworks_file)
    elif json_corpus_path is not None and not os.path.isdir(json_corpus_path):
        print("the path to the directory of source JSON files is not valid: ", json_corpus_path)
    elif tei_corpus_path is not None and not os.path.isfile(tei_corpus_path):
        print("the path to the source corpus TEI XML file is not valid: ", tei_corpus_path)
    elif json_corpus_path is not None:
        enrich_tei_files_via_json(tagworks_file, json_corpus_path, output_path)
    elif tei_corpus_path is not None:
        enrich_tei_files_via_tei_corpus(tagworks_file, tei_corpus_path, output_path)    
