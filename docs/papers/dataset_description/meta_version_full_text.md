Motivation and Prior Work

Researchers and industry are increasing labeling (or annotating) data to facilitate machine learning. Drawing on and adapting qualitative content analysis techniques. Little formalized guidance available. Data annotation is also rediscovering some challenges of data provenance familiar to the information sciences.

The goal of this paper is thus two-fold: to present a labeled dataset, and to reflect on the process and challenges in its creation and presentation. To meet these goals we present three sections. The first is a paper within a paper, straightforwardly describing our annotation project and its results. The second provides substantial process and provenance description (including mis-steps and detailed decisions). The third reflects on the overall process, describing tensions experienced and highlighting areas where information science can provide further guidance for supervised machine learning dataset creation projects.

# Genre paper: a gold standard dataset on software mentions in the scientific literature

We present an annotated dataset of software mentions in full-text scientific papers converted from PDFs of academic articles. The dataset provides a "gold-standard" training/testing set for developing supervised machine learning to accomplish named entity recognition at scale.

First we discuss motivations and prior work on named entity recognition of software, describe our coding scheme and reliability checks, present the dataset file (format and contents). Finally we briefly demonstrate the usefulness of the dataset and discuss future work.

## Motivations and prior work on software named entity recognition

Software is crucial to scholarship, forming a "knowledge infrastructure" that supports and enables research (cite Mayernik et al.). Yet, researchers are often frustrated by redundant, incompatible, or poorly supported pieces of software. Like other infrastructural work, the creation and maintenance of research software has been found to be relatively invisible, especially to the formalized scholarly reputation system built on bibliometrics. This is because software is rarely formally cited (cite Howison and Bullard). If we were able to more accurately identify the use of software in the published literature, we could make software infrastructural contributions more visible, creating a resource for demonstrating impact. Such a resource would be valuable to both those doing the software work and to those seeking to identify and fund needed software work to improve scholarship.

Ongoing work addresses making software visible in the academic literature in two ways. The first is to create and disseminate clear standards for citation, changing the behavior of authors and publishers. The second, known as named entity recognition, is to work with existing published literature (and that to be published while standards propagate) to automatically identify software, however it is mentioned.

named entity recognition is challenging, but has been successful across a range of entity types, including XXXX. Challenges involved are: the diversity of language used to reference entities, the lack of a controlled vocabulary or namespace for naming entities. Supervised machine-learning is a promising approach, but requires substantial datasets for training and testing.

Further challenges to useful systems based on named entity recognition come from the form of academic publishing. First, only a small portion of the published literature is available in clean full text, such as marked up XML. The baseline form of literature is the academic PDF, which are challenging to convert to text for machine processing. Thus named entity recognition is often limited to abstracts and targeted to literature discovery rather than full scale "distant reading" (cite Moretti/Mehta et al.) for bibliometrics and analysis of the literature at scale.

A recent review article (Krüger and Schindler, 2020) provides an analysis of prior work on named entity recognition of software mentions ("software usage statements"). They identify 48 studies using four techniques, in increasing complexity: 1) Term Search, 2) Manual Extraction, 3) Rule-based Extraction, and 4) Supervised Learning. Term Search, employed in 12 articles, involves searching databases for known strings, such as URLs, DOIs, or particular software names. Manual Extraction, used in 16 studies, involve "approaches in which humans read a text in order to identify usage statements" but which are not then used for machine learning training/testing. Rule-based extraction, used by 16 articles, involves non-machine learning approaches, usually rules pre-specified by humans. For example, using regular expression matching, "special spellings such as capitalization", or "the appearance of special words indicating artifacts", informed by human experts. (cite BioNerDs). Rule-based extraction can be used to generate training/testing datasets for machine learning, including "distant supervision" and "weak supervision" through iterative bootstrapping (discussed further below). Finally supervised learning employs a manually annotated and curated "gold standard" dataset of software mentions to train a classifier.

The four techniques generally show a trade-off between scope, performance, and cost. For example, term search for specific software, but likely to have high performance, but is obviously of scope limited to the specific software searched. Manual annotation for specific software has wider scope, in that it can recognize alternative forms of mentioning the searched for software, but higher cost due to greater human reading requirements (cite HubZero paper). Rule-based extraction can be of high performance but with scope limited to specific domains or types of software with practices that leave identifiable artifacts in papers. For example BioNerDs (XXXXX check these numbers) showed precision of 0.49 and recall of 0.57, while rules specific to the R statistics software ecosystem, showed precision of 0.84 and recall of 0.87, drawing heavily on URL formats specific to R package management (XXXX check me). Rule-based extraction involves cost in designing the rules, but low cost of re-use across larger datasets.

Iterative boostrapping uses expert specified rules to identify an initial set of software mentions (as "seeds"), then using those as training examples for supervised machine learning to identify further examples for manual review, expanding the training set. Bootstrapping can provide high precision, but relatively low recall (e.g., Pan et al achieved precision of 0.83 but recall of 0.35). Recall is limited due to the incomplete coverage of identifying patterns of language use. In the language of content analysis, the initial seeds do not achieve saturation, even when complemented by expansion through machine learning. Evaluation of "distant" or "weak" supervision is expensive because while false-positives can be identified through review of the results (a relatively small amount of text), false-negatives require exhaustive manual review of full-text. That manual review increases the cost of bootstrapping, but is key to evaluation.

Supervised machine learning based on manually annotated "gold standard" datasets shows the most generalizable scope and flexibility, good performance. For example demonstration use of deep learning on a dataset of 85 annotated articles (in a specific domain) showed precision of .90 and recall of .94. These come at high cost both in the initial creation of the gold standard dataset and in computation costs for more advanced techniques. While different supervised machine learning algorithms (e.g., CRF, sequence models, SVMs, neural networks, deep learning, etc.) can boost performance the size of the gold standard manual annotation is important (cite something about ImageNet). Existing published datasets, all using slightly different annotation schemes, have annotated 90 (Howison and Bullard), 40 (Nangia and Katz), 166 (Allen et al), and 85 articles (Duck et al).

For these reasons we created a manually annotated dataset of software mentions on full-text derived automatically from academic PDFs. This dataset will be useful both for training supervised models and for evaluating bootstrapping techniques (which could then be used to further expand available training or specialize to a specific otherwise troublesome domain). We annotated XXXX4,973 PDFs, identifying XXXX7,024 mentions of software. Those mentions were found in XXXX1,247 articles (XXXX3,726 articles had no mentions, providing copious negative examples) (XXXX these numbers should come directly from Rtex queries of the published TEI XML files). We therefore provide a gold standard dataset significantly larger than those previously available, and one aligned with a high-quality, freely available extraction tool for academic PDFs and therefore likely to generalize.

For each mention we annotated details:  (full coding scheme is available online).

Summary figures and examples.

The dataset is published as a single TEI XML file, including identifiers for each paper, metadata on the papers. Mentions are encoded using `<rs >`, as shown in Figure XXXX.

Paper selection and conversion by GROBID.

Our annotation was done by XXXX24 annotators over YYYY2 year time period. After training of our annotators, KKKK articles were doubled-coded, showing agreement at XXXX. After talking to agreement as a group, then adjusting our coding scheme, articles were then singly coded by our trained annotators. At the conclusion of annotation, the full dataset of annotations was then reviewed by the authors (who are domain specialists on scientific software) resulting in curation adjustments made for consistency across the dataset. For example, expert review removed annotation of web services like Google and standardized on excluding strings like "v." and "version" from the software_version field. Finally, we used string searches of the mentions discovered across our full dataset, identifying a small number of annotations missed due to annotator fatigue or training inconsistency. Details on curation of the full dataset are in our full coding scheme, published online XXXX.

## Prototype use for supervised machine learning

We demonstrate the usefulness of this dataset by using it for training/testing a basic supervised machine learning system.

As expected a relatively simple supervised model (CRF) shows good performance, when compared to bootstrapping. This is particularly true for recall.

It is a goal of our work to generate community interest and collaboration. We hope that the community will use this dataset for further improvement, including using computationally expensive algorithms such as BlistXXXX. We anticipate that the larger dataset should enable training systems of equivalent or better performance to that of Kruger (cite), but more robust to novel data and domains. To encourage others we do not report results from more computationally complex models, leaving "low hanging fruit" to encourage collaboration (cite Raymond.)

## Future work

We have provided a dataset of mentions of software in the academic literature. It is the largest dataset available to date, and is derived from full text of articles that have been converted directly from published academic PDFs. This makes the dataset useful for supervised machine learning at scale.

Our future work takes two forms: collaborative expansion of the dataset and use of large scale databases of mentions discovered by systems trained on the dataset.

First we are founding a community project to further increase the size and scope of the dataset. This involves adapting existing annotated corpuses for consistency with our scheme, collaboratively annotating articles in new domains, and using the gold standard to validate promising bootstrapping techniques to further increase available training/testing examples.

Second we are using the dataset to perform machine learning at scale and prototying three systems that use the resulting dataset of mentions. Our prototype scaled system will be used to develop "Software Impact Story" a companion to the alt-metrics enabled "Impact Story" providing suggested mentions of software developed by individuals. Softcite suggest is a prototype citation recommendation system, analyzing submitted manuscript text to highlight uncited mentions and to suggest unmentioned software that similar articles have used. Finally, discovered mentions will be deployed in the CiteAs.org system. CiteAs is a specialized search engine that takes the name or identifier of software, and returns a suggested citation. Currently CiteAs uses web crawling and conventions such as CITATION files in repositories to discover author's preferred citations. Software mentions in publications will provide additional sources. We expect that the diversity of mention forms for software—which causes trouble for impact assessment—will encourage software contributors to make clearer requests for citation.

# How the dataset was created

In this section we describe the process of creating the SoftCite dataset in greater detail. The provenance of datasets is crucial to their appropriate use, as machine learning models trained in one context will return errors if applied to another [@gebru_datasheets_2020], including reproducing social biases. Additionally we hope that relatively rich detail in our account will offer methodological guidance to those researchers undertaking the creation of datasets.



Recent literature
    - Starts with process figure (consider a little more timeline?)
    - includes abandoned work/recoveries.

3. Tensions and Reflections about creation
    - Reliability vs speed/size
        - Unclear where saturation in training/location of issues to train about, thus post-annotation curation is key.
        - Limited guidance on "consistency" phase. What is acceptable/problematic (and why?)
    - Provenance vs usefulness
        - very hard to predict??
        - opens up criticism??
    - Presenting dataset as artifact vs process
        - genre expectations
        - hard to know how much to describe (cite Ribes article, but also cite data sharing literature)
    - Openness vs fear of being scooped
