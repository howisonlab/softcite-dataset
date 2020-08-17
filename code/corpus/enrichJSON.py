"""
    Inject software mention annotations into articles in JSON format (converted from TEI XML format via TEI2LossyJSON.py) into into the JSON. 
    Two methods are available:
    1) dictionary/whitelist term lookup
    2) call of the Softcite software mention service
"""

import os
import argparse
import ntpath
import json
from collections import OrderedDict
import pysbd
import re

class Annotator(object):    

    def __init__(self, config_path='./config.json'):
        # load config and white term list
        self.config = self._load_config(config_path)

        white_list_files = self.config["whitelist"]
        whitelist = []
        for file_string in white_list_files:
            print(os.path.join("../../data/software_lists/go", file_string))
            with open(os.path.join("../../data/software_lists/go", file_string)) as file:
                # these are actually text files, one term per line (no comma/tab separation)
                line = file.readline()
                while line:
                    if len(line.strip()) == 0:
                        continue
                    if not line.strip() in whitelist:
                        whitelist.append(line.strip())
                    line = file.readline()
        black_list_files = self.config["blacklist"]
        for file_string in black_list_files:
            print(os.path.join("../../data/software_lists/stop", file_string))
            with open(os.path.join("../../data/software_lists/stop", file_string)) as file:
                line = file.readline()
                while line:
                    if len(line.strip()) == 0:
                        continue
                    if line.strip() in whitelist:
                        whitelist.remove(line.strip())
                    line = file.readline()
        print("total", str(len(whitelist)), "terms")
        self.whitelist_matcher = re.compile(r'\b(?:%s)\b' % "|".join([re.escape(x) for x in whitelist]))

    def _load_config(self, path='./config.json'):
        """
        Load the json configuration 
        """
        config_json = open(path).read()
        return json.loads(config_json)

    def match_term(self, text):
        positions = []
        for match in re.finditer(self.whitelist_matcher, text):
            #groups = match.groups()
            #for idx in range(0, len(groups)):
            #print(match.start(), match.end())
            positions.append([match.start(), match.end()])
        return positions

    def inject_corpus_annotations(self, method, json_path, output_path):
        for file in os.listdir(json_path):
            if file.endswith(".json"):
                print(os.path.join(json_path, file))
                with open(os.path.join(json_path, file)) as jsonfile:
                    json_doc = json.load(jsonfile, object_pairs_hook=OrderedDict)
                    new_doc = OrderedDict()
                    document_id = None
                    if "id" in json_doc:
                        document_id = json_doc["id"]
                        new_doc["id"] = json_doc["id"]
                    if "abstract" in json_doc:
                        new_doc["abstract"] = json_doc["abstract"]
                    if "body_text" in json_doc:
                        rank = 0
                        new_doc["body_text"] = []
                        for paragraph in json_doc["body_text"]:
                            text = paragraph["text"]
                            entities = None
                            references = None
                            if "entity_spans" in paragraph:
                                entities = paragraph["entity_spans"] 
                            else:
                                entities = []
                            if method == 'whitelist' or method == 'all':
                                spans = self.match_term(text)
                                if spans is not None and len(spans) > 0:
                                    for span in spans:
                                        entity = OrderedDict()
                                        entity['type'] = 'software'
                                        entity['start'] = span[0]
                                        entity['end'] = span[1]
                                        entity['rawForm'] = text[span[0]:span[1]]
                                        entity['resp'] = "whitelist"
                                        if document_id is not None:
                                            entity['id'] = document_id + "-"
                                        else:
                                            entity['id'] = ''
                                        entity['id'] += "software-simple-w" + str(rank)
                                        rank += 1
                                        entities.append(entity)
                            if method == 'service' or method == 'all':
                                json_results = self.software_mention_service(text)
                            if len(entities)>0:
                                paragraph["entity_spans"] = entities
                            new_doc["body_text"].append(paragraph)

                    output_file = os.path.join(output_path, file)
                    with open(output_file, 'w') as outfile:
                        json.dump(new_doc, outfile, indent=4)  

    def software_mention_service(self, text):
        return {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Inject automatic software mention annotations into fulltext in lossy JSON format")
    parser.add_argument("--method", type=str, 
        help="method for producing the annotations")
    parser.add_argument("--json-repo", type=str, 
        help="path to the directory of JSON files converted from TEI XML produced by GROBID, where to inject the automatic annotations")
    parser.add_argument("--output", type=str, 
        help="path to an output directory where to write the enriched JSON file(s)")
    parser.add_argument("--config", default="./config.json", help="path to the config file, default is ./config.json") 

    valid_methods = ['whitelist', 'service', 'all']

    args = parser.parse_args()
    method = args.method
    json_repo = args.json_repo
    output_path = args.output
    config = args.config

    if method not in valid_methods:
        print('error: method must be one of', valid_methods)
        exit(0)

    # check path and call methods
    if json_repo is None or not os.path.isdir(json_repo):
        print("error: the path to the JSON files is not valid: ", json_repo)
        exit(0)

    annotator = Annotator(config)
    annotator.inject_corpus_annotations(method, json_repo, output_path)

