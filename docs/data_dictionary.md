# Data Dictionary: Softcite dataset

Raw annotation data repository: https://github.com/howisonlab/softcite-dataset

Annotators tagged software mentions by articles. For each article they documented their annotation results in a single RDF file (i.e., each RDF file is an annotator-article level input), named as "annotator_id-article_id.ttl". Each article, annotator, and software mention, have its unique identifier in each RDF file. All the RDF files are locted in `data/individuals-*`.

<<<<<<< HEAD
RDF file schema:
	For each article annotators document
		`codable`: if the article is in English and human-readable
		`standard_type`: if the article is a regular academic article with reference
		`coded_no_in_text_mentions`: if the article does not contain software mentions in its body text

		Each software mention is an `in_text_mention` with the following annotation fields:
			`full_quote`: the text span where the software mention is identified
		`tei_full_quote`: added during post-processing for text aligning purpose. Counterpart of `full_quote` in TEI XML text 		conversion of original PDF articles.
			`on_pdf_page`: location indicator for text aligning consideration
			`spans_pages`: if the software mention goes across the page break
			`mention_type`: software, or other annotator defined categories such as dataset, database, hardware, etc.
				A self-rated `certainty` score is attached within this field, ranging from 1 to 10 (integer)
				A free-text `memo` field is accompanied for documenting annotator reasoning for judgment.
			`software_was_used`: if the software is used in the research discribed in the article
			`software_name`
			`version_number`
			`version_date`
			`url`
			`creator`
			`has_reference`: if the software mention has a reference entry.

		The `reference` linked to `in_text_mention` contains the following annotation fields:
			`full_quote`: the full reference entry corresponding to the software mention in body text.
			`on_pdf_page`
			`spans_pages`
			`reference_type`: select one from 4 options: publication/user_guide/project_page/project_name
			`software_name`
			`version_number`
			`version_date`
			`url`
			`creator`

All the individual RDF input are parsed into a rectangular dataset in CSV format, located in data/csv_dataset.

CSV data schema:
	`softcite_articles.csv`: article,article_set,coder,no_selections_found
	`softcite_codes_applied.csv`: selection,coder,code,was_code_present,code_label
	`softcite_in_text_mentions.csv`: selection,coder,article,quote,tei_quote,page,mention_type,certainty,memo
	`softcite_references.csv`: reference,from_in_text_selection,article,quote,coder,page,reference_type

After expert review, we have an aggregated dataset in TEI XML format, each software mention only has one final adjudicated annotation and is presented in its context paragraph. The TEI XML dataset include article level metadata for identifying annotated academic articles. Each annotated software mention is associated with an `xml:id` as its unique identifier linking to the corresponding article. The annotation of software mention in TEI XML corpus also include annotator id, type(software/version/publisher/url). Note that `version_date` and `version_number` have been merged into `version`; `creator` has changed to `publisher` (just a field title change). All the annotation that has been modified during expert review has a `curator` identifier associated.
=======
### RDF data schema

For each article annotators document:
- `codable`: if the article is in English and human-readable
- `standard_type`: if the article is a regular academic article with reference
- `coded_no_in_text_mentions`: if the article does not contain software mentions in its body text

Each software mention is an `in_text_mention` with the following annotation fields:  
- `full_quote`: the text span where the software mention is identified
- `tei_full_quote`: added during post-processing for text aligning purpose. Counterpart of `full_quote` in TEI XML text conversion of original PDF articles.
- `on_pdf_page`: location indicator for text aligning consideration
- `spans_pages`: if the software mention goes across the page break
- `mention_type`: software, or other annotator defined categories such as dataset, database, hardware, etc.
	- A self-rated `certainty` score is attached within this field, ranging from 1 to 10 (integer)
	- A free-text `memo` field is accompanied for documenting annotator reasoning for judgment.
- `software_was_used`: if the software is used in the research discribed in the article
- `software_name`
- `version_number`
- `version_date`
- `url`
- `creator`
- `has_reference`: if the software mention has a reference entry.

The `reference` linked to `in_text_mention` contains the following annotation fields:
- `full_quote`: the full reference entry corresponding to the software mention in body text.
- `on_pdf_page`
- `spans_pages`
- `reference_type`: select one from 4 options: publication/user_guide/project_page/project_name
- `software_name`
- `version_number`
- `version_date`
- `url`
- `creator`

All the individual RDF input are parsed into a rectangular dataset in CSV format, located in `data/csv_dataset`.

### CSV data schema

- `softcite_articles.csv`: article-level annotation metadata. Fields included: article, article_set, coder, no_selections_found.
	- `article`: unique identifier of research articles being annotated. For PMC article set it is the PMCID; for the Econ article set it is the article DOI.
	- `article_set`: source of articles.
	- `coder`: unique identifier of annotators.
	- `no_selections_found`: If there is text selections that contains software mention(s) found in the article. Boolean valued.

- `softcite_codes_applied.csv`: for each selection what entities were annotated by whom. Fields included: selection,coder,code,was_code_present,code_label
	- `selection`: unique identifier of the text selection that contains software mention(s).
	- `code`: types of entities we are annotating, including `software_was_used`, `software_name`, `version_number`, `version_date`, `url`, `creator`.
	- `was_code_present`: if the entity type exists in the text selection. Boolean valued.
	- `code_label`: annotated text for the corresponding entity type. Selected from the article text.

- `softcite_in_text_mentions.csv`: text spans selected from a PDF article and the mentions contained within the text. Fields included: selection,coder,article,quote,tei_quote,page,mention_type,certainty,memo
	- `quote`: text selection. The text span selected from the article text that contains annotated entities.
	- `tei_quote`: corresponding text selection selected from the TEI XML conversion of the annotated article. Added during the post-processing after the first-round annotation.
	- `page`: on which page of the original PDF article the text selection is located.
	- `mention_type`: Does the mention annotated refer to software? Free text entry of other entity types is allowed. Existing entity types include software, database, etc.
	- `certainty`: self-rating of how certain annotators are about whether the mention annotated is software. An integer value ranges from 1 to 10.
	- `memo`: free text memoing of annotator reasoning about the mention type.

- `softcite_references.csv`: reference,from_in_text_selection,article,quote,coder,page,reference_type
	- `reference`: unique identifier of the reference item being annotated.
	- `from_in_text_selection`: unique identifier of the text selection in the article body text with which the reference item is linked.
	- `quote`: text selection of the reference item.
	- `page`: on which page of the original PDF article the text selection of the reference item is located.
	- `reference_type`: what does the reference item refers to, types including `publication`, `project_name`, `project_page`, `user_guide`.

### TEI XML data schema

After expert review, we have an aggregated dataset in TEI XML format, each software mention only has one final adjudicated annotation and is presented in its context paragraph. The TEI XML dataset includes article level metadata for identifying annotated academic articles. Each annotated software mention is associated with an `xml:id` as its unique identifier linking to the corresponding article. The annotations of software mention in TEI XML corpus also include annotator id and entity type(software/version/publisher/url). Note that `version_date` and `version_number` have been merged into `version`; `creator` has changed to `publisher` (just a field title change). All the annotations that has been modified during expert review have a `curator` identifier associated.

Current aggregated dataset is here: https://github.com/ourresearch/software-mentions/blob/master/resources/dataset/software/corpus/all_clean_post_processed.tei.xml
>>>>>>> c27f277c86079d90f89b8c9509e0c1e0915abef0
