# Softcite dataset

**A gold-standard dataset of software mentions in research publications for supervised learning based named entity recognition**


## Why creating this dataset
Software lays a critical foundation for measureless research activities today. However, researchers are often frustrated by redundant, incompatible, or poorly supported pieces of software ([Howison et al., 2015](https://academic.oup.com/rev/article/24/4/454/1518466)). One pathway to improve software for research is to increase the visibility of software in the bibliometric-based system of research impact. So that software contributions to research can be well acknowledged, software creators, funders, and other stakeholders have more incentives to cooperate and provide more sound, quality-assured software work.

We have spent the past years on the manual annotation of ~5k open access research publications in areas of life sciences and social sciences. As a result, we annotated 5,171 software mentions in published research. Largely these software mentions are not indexed, formal citations ([Howison & Bullard, 2016](https://asistdl.onlinelibrary.wiley.com/doi/pdf/10.1002/asi.23538?casa_token=2HjchVhidz8AAAAA:kHyNwZA_kwysafi_7_H3HtcBCAhAgqG96LB9z0_iNtv1lviA7Xo1riWv59IEx-_8hLGVq2SU_iMkGg)). So we have ferreted out a lot of software that contribute to research but currently are not visible to academic databases and systems of information retrieval.

## Dataset content
Our [released dataset](https://raw.githubusercontent.com/howisonlab/softcite-dataset/master/data/corpus/softcite_corpus-full.tei.xml) is a TEI/XML corpus file that contains metadata of annotated research publications and software mentions identified in these publications. The software mentions are further annotated with details about the software, including software `version`, `publisher`, and access `url`, if present in the publication text. The annotated software mentions are presented in their paragraph context considering that they are contextual specific. Below is an example of software mentions in annotated publication with all metadata encoded with the TEI/XML schema. You can find thousands of entries like this in the Softcite dataset.

![snapshot of an annotated article entry with encoded software annotations in the Softcite dataset](https://raw.githubusercontent.com/howisonlab/softcite-dataset/master/docs/images/tei_entry_ex.png)

## Use scenarios
We created the Softcite dataset in a machine-readable (TEI/XML) format for immediate machine learning use. It is designed to accommodate training/validation for supervised learning based scholarly text mining. You could use it to train your model for software entity recognition in text, to develop utilities for increasing software visibility to information systems, or to investigate how software has been used for research. We have prototyped machine learning training ourselves and validated that the Softcite dataset is effective for machine learning use. If you need help for a safe jumpstart for your project, feel free to contact [Fan Du] [mailto:cfdu@utexas.edu]. We advocate the proper use of all data.

## The Softcite approach
Understanding data provenance is important for data reuse. We have [a forthcoming publication](https://github.com/howisonlab/softcite-dataset/raw/master/docs/papers/Softcite_Dataset_Description_RC.pdf) that details the design consideration and creation process of the Softcite dataset. It also documents the annotation schema of the Softcite dataset.

To ensure data consistency across the whole pipeline, we used [GROBID](https://github.com/kermitt2/grobid), an open source machine learning library, to convert thousands of open access publication PDFs into TEI/XML text. Our annotation team consists of experts in NLP and research software, and students from UT Austin who had been through group training. (Training materials can be consulted [here](https://howisonlab.github.io/softcite-dataset/)) The annotation team read through every PDF publication, annotated mentions of software and their details. We conducted an inter-annotator agreement check to ensure training was effective. We collected all the annotation data input from annotators via GitHub and validated the incoming data via a test suite deployed on Travis CI, coupled with senior annotators' manual examination.

After the annotation, we checked the annotation consistency across the whole dataset via a script and expert review. All the software mentions in the Softcite dataset have been reviewed by expert annotators, ensuring its gold standard quality. We encoded the annotations in the converted TEI/XML article text using GROBID.

![from annotated PDFs to TEI/XML corpus](https://raw.githubusercontent.com/howisonlab/softcite-dataset/master/docs/images/pdf-tei-annotated-example.png)

## Release and Change
See our [changelog](https://raw.githubusercontent.com/howisonlab/softcite-dataset/master/CHANGELOG.md).

## Implementation
We have utilized the Softcite dataset to train a set of machine learning models and implemented them as a [GROBID module for software mention recognition](https://github.com/ourresearch/software-mentions). The software mention recognizer is further used to seed a Software Knowledge Base. The Software Knowledge Base provides capabilities such as software entity extraction, disambiguation, citation information retrieval, and cross-entity inference. A [REST API](https://github.com/kermitt2/softcite-api) is provided for leveraging the Software Knowledge Base.

## Roadmap
* We hope to build interoperability with other existing datasets and resources about software mentions in scientific text. Interoperable datasets can scale up ML-based efforts for software entity recognition and increasing research software visibility.
* We also have developed [CiteAs.org](http://citeas.org/) in collaboration with [Our Research](https://our-research.org/). [CiteAs.org](http://citeas.org/) is an interactive search engine for discovering software and other research outputs online. It offers citation recommendation and provenance according to your search query, and our goal is to integrate the Software Knowledge Base into [CiteAs.org](http://citeas.org/) for enhanced recommendation capability.
* We have crowdsourced more software annotation data based on our annotation scheme in different domain literature. We expect to release these data for the community working on software entity recognition in the future.

If you have suggestions, comment, welcome to contact [Fan Du](mailto:cfdu@utexas.edu), or start an issue in the repository.

## License
The Softcite dataset is released under [CC-BY-4.0 license](https://creativecommons.org/licenses/by/4.0/).
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.

## Acknowledgement
We thank Alfred P. Sloan Foundation for supporting this work. We also appreciate our collaborators and student annotators for making this dataset gold standard and available.
