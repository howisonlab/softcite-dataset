Motivation and Prior Work

Researchers and industry are increasing labeling (or annotating) data to facilitate machine learning. Drawing on and adapting qualitative content analysis techniques. Little formalized guidance available. Data annotation is also rediscovering some challenges of data provenance familiar to the information sciences.

The goal of this paper is thus two-fold: to present a labeled dataset, and to reflect on the process and challenges in its creation and presentation. To meet these goals we present three sections. The first is a paper within a paper, straightforwardly describing our annotation project and its results. The second provides substantial process and provenance description (including mis-steps and detailed decisions). The third reflects on the overall process, describing tensions experienced and highlighting areas where information science can provide further guidance for supervised machine learning dataset creation projects.

# Genre paper: a gold standard dataset on software mentions in the scientific literature

We present an annotated dataset of software mentions in full-text scientific papers converted from PDFs of academic articles. The dataset provides a "gold-standard" training/testing set for developing supervised machine learning to accomplish entity extraction at scale.

First we discuss motivations and prior work on software entity extraction, describe our coding scheme and reliability checks, present the dataset file (format and contents). Finally we briefly demonstrate the usefulness of the dataset and discuss future work.

## Motivations and prior work on software entity extraction

Software is crucial to scholarship, forming a "knowledge infrastructure" that supports and enables research (cite Mayernik et al.). Yet, researchers are often frustrated by redundant, incompatible, or poorly supported pieces of software. Like other infrastructural work, the creation and maintenance of research software has been found to be relatively invisible, especially to the formalized scholarly reputation system built on bibliometrics. This is because software is rarely formally cited (cite Howison and Bullard). If we were able to more accurately identify the use of software in the published literature, we could make software infrastructural contributions more visible, creating a resource for demonstrating impact. Such a resource would be valuable to both those doing the software work and to those seeking to identify and fund needed software work to improve scholarship.

Ongoing work addresses making software visible in the academic literature in two ways. The first is to create and disseminate clear standards for citation, changing the behavior of authors and publishers. The second, known as entity extraction, is to work with existing published literature (and that to be published while standards propagate) to automatically identify software, however it is mentioned.

Entity extraction is challenging, but has been successful across a range of entity types, including XXXX. Challenges involved are: the diversity of language used to reference entities, the lack of a controlled vocabulary or namespace for naming entities. Supervised machine-learning is a promising approach, but requires substantial datasets for training and testing.

Further challenges to useful systems based on entity extraction come from seeming the form of academic publishing. First, only a small portion of the published literature is available in clean full text, such as marked up XML. The baseline form of literature is the academic PDF, which are challenging to convert to text for machine processing. Thus entity extraction is often limited to abstracts and targeted to literature discovery rather than full scale "distant reading" (cite Moretti/Mehta et al.) for bibliometrics and analysis of the literature at scale.

Existing work on entity extraction for software ...
Mechanistic techniques (whitelists, regex matching for repos)...
These mechanistic techniques can be used further to generating a dataset of mentions for training/testing. This approach is called "bootstrapping" where a sub-set of mentions are found automatically, and then used to train/test a supervised machine learning system which can discover entities not found mechanistically. However, bootstrapped datasets are challenging to assess for recall, since one can only review the suggested annotations for false positives. Reviewing the full dataset for false negatives is only possible by reviewing the full dataset (negating the advantages of boostrapping).

For these reasons we created a manually annotated dataset of software mentions on full-text derived from academic PDFs. We annotated XXXX PDFs, finally identifying XXXX mentions of software in XXXX articles (XXXX had no mentions). For each mention we annotated details:  (full coding scheme is available online).

Summary figures and examples.

The dataset is published as a single TEI XML file, including identifiers for each paper, metadata on the papers. Mentions are encoded using <rs >, as shown in Figure XXXX.

Paper selection and conversion by GROBID.

Our annotation was done by XXXX coders over YYYY time period. After training of our annotators, KKKK articles were doubled-coded, showing agreement at XXXX. After adjustment of the coding scheme, articles were then singly coded by our trained annotators. At the conclusion of annotation, the full dataset of annotations was then reviewed by the authors (who are domain specialists on scientific software) and with adjustments made for consistency across the dataset. For example, expert review removed annotation of web services like Google and standardized on excluding strings like "v." and "version" from the software_version field. Details on curation of the full dataset are in our full coding scheme, published online XXXX.

## Prototype use for supervised machine learning

We demonstrate the usefulness of this dataset by using it for training/testing a basic supervised machine learning system.

While we hope that the community will use this dataset for further improvement, these results are already improvements on prior work.

## Future work

We have provided a dataset of mentions of software in the academic literature. It is the largest dataset available to date, and is derived from full text of articles that have been converted directly from published academic PDFs. This makes the dataset useful for supervised machine learning at scale.

Our future work takes two forms. First we are founding a community project to increase the size of the dataset. Second we are using the dataset to perform machine learning at scale and prototying two systems that use the resulting dataset of mentions.

We have contacted groups who have undertaken similar annotations (discussed above in prior work) and are working (on github) to integrate these into a shared dataset.

Our prototype scaled system will be used for Software Impact Story, CiteAs, and Softcite Suggest.

2. Provenance Presentation
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
