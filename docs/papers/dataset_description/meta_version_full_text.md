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

# Creation of the dataset

In this section we describe the process of creating the SoftCite dataset in greater detail. The provenance of datasets is crucial to their appropriate use, as machine learning models trained in one context will return errors if applied to another [@gebru_datasheets_2020], including reproducing, or even exacerbating, social bias. Additionally we hope that relatively rich detail in our account will offer methodological guidance to those researchers undertaking the creation of datasets.

As one reads this section some details may seem irrelevant or extraneous. Be assured that, as authors, we were often unsure what details to include. More, as you read, you may find details that undermine the impression of quality hopefully conveyed by the bare-bones presentation above. In the final section of this paper we reflect on the process, and emotions, of documenting our process and writing this section.

## Genesis of the project

The creation of this dataset followed the publication of Howison and Bullard [@howisonandbullard], which examined 90 articles from the literature, documenting low rates of formal citation suggested by earlier interviews with researchers who build software, where the interviews had been focused on incentives for software work and maintenance. The software mentions found in those articles formed the initial training examples. Two elements of the coding scheme are clearly linked to these origins, and might not be present in dataset creation processes for named entity extraction.

The first was the `software_used` tag, which indicating whether it seemed that the authors actually used the mentioned software in their work. The second was effort to connect in-text mentions with nearby citations, and to code the type of article cited in the linked reference.

## Selection of papers

It was key to the motivations for the project that any system ultimately be able to process PDFs, because we wanted to be able to process historical publications and publications yet to adopt any improved software citation policies. However, at the origins of the project we did not know about the `GROBID` tool for converting academic PDFs. We experimented with `pdf2text` (and the rOpenSci package, `fulltext`) [XXXXcite] but found the output too inconsistent to be readable as an article, undermining annotators engagement and contextual understanding.

We also wanted to be able to release a dataset that others could work with. This explains our choice to annotate open access articles, avoiding creating a dataset that annotates proprietary article collections from publishers. While not all articles could be republished in converted fulltext form, we reasoned that future users would be able to obtain the fulltext via the DOI.

Accordingly we started with PubMed Open Access, particularly because it provided XML versions of the article. However, given our ultimate intent to work with converted PDF fulltext, we did not provide the XML versions of the articles to annotators (since we would not be able to do that later). We did, as discussed below, use the available XML text for our first round of agreement coding. Having students select quotes directly from PDF articles was a risky decision; team-members disagreed about how hard it would be to later alignment these quotes with converted fulltext. Indeed alignment was difficult, causing long-running difficulties, although the discovery of GROBID helped immensely.

## Collaboration infrastructure

Our annotators used text editors to enter details into text files, formatted as RDF in Turtle format (cite). These files were generated by an article assignment process driven by a command line script, talking to a `mysql` database which kept track of which articles had been assigned to which annotators. Annotators edited these files, using keyboard shortcuts to insert "snippets" which were text templates for each step of the annotation.

These files were then checked into github, using the commandline git client and creating pull requests, which were accepted by doctoral student members of the research team. Each annotator worked in a folder named for their user, to avoid file editing conflicts. A python script (XXXXURL) was used to read all the RDF into a single RDF graph (full_dataset.ttl). Typos, unfilled fields, and RDF Turtle syntax errors were a frequent issue. Later we implemented continuous integration using TravisCI on github pull requests to check syntax and validate responses; we hoped that annotators would fix these when alerted by the pull request, but they almost always required help to both resolve the identified issues and to manage confusion over what work was "in" a pull request. When analyses began, we used SPARQL queries (citeXXXX) to export the dataset in CSV format.

The majority of annotation was done on a department Linux server with annotators provided command line user accounts and thus home directories. Annotators used the Atom editor running on their laptop to edit files on the server, mounted via SFTP provided by Atom.

We used this rather idiosyncratic infrastructure for three reasons. First, we intended to annotate the in-text mention and linked references as units, following the Howison and Bullard publication. This made existing content analysis tools, such as Atlas.TI (cite) harder to use. Second, we knew the project would take considerable time and we did not want to rely on hosted commercial annotation tools that might change in ways that undermined the project (and believed that github, at least in basic functions, was relatively stable.) Third, we chose to use git-based aggregation approach rather than building a custom web-UI because we reasoned the effort to train the student annotators would be valuable to them as students and us as educators, while the effort to build and maintain a web-UI would be equally large but of benefit only to those building it (as well as likely being fragile). We used SFTP mounted files because we wanted all work, even that in progress, to be in a file-space owned by the project and thus able to be backed up even prior to students submitting via git. Indeed, after the main phase of annotation, while checking our assignment database against work completed, we found some un-submitted work in annotator home folders (which we, as admins, submitted via git).

Annotators were recruited by advertising a research project in university venues. They were paid $15 an hour but restricted to 10 hours a week. Some wanted to work more, but we felt it was important to prevent fatigue and maintain some balance between annotator contribution level. Students were largely from a large public university (XXXXblinded) but we recruited a small number from a local historically black  university, with a large hispanic population. Unexpected issues with work authorization documentation (required of those not students at our institution, but not those already students) meant those HBCU students were not able to contribute many annotations.

Students were trained in classrooms, with materials prepared by a doctoral student and published on our github site (where they remain, blindedXXXX). These materials addressed both our collaboration infrastructure and our annotation scheme. We first used the articles coded in the Howison and Bullard paper. We coded a number of files all together, including allowing and encouraging open questions, before breaking into groups. In later weeks, we conducted training for newly recruited annotators, with previously trained annotators working in pairs on assigned articles on one side of the large room. All were encouraged to get involved in discussions, or bring questions to the group. The PI was deferred to as the authority or oracle, with doctoral students writing down reasoning and testing it in open conversation. Despite efforts, new examples often lead to referring to the PI but the PIs responses were sometimes inconsistent over time. It was challenging to managing training, assignment logistics, payroll, and reason about specific examples. It was also challenging to encourage annotators to disagree in public. As these discussions were face to face, there are no records other than those ultimately encoded in the annotation scheme as examples and justifications. Evolution of the annotation scheme could be somewhat recovered by examining the git log history of the scheme and the training pages.

After initial training on articles assigned to all, annotators were assigned articles in pairs, such that each article was annotated by two annotators, managed by updates in the `mysql` database. After our first round of agreement assessment each article was assigned to only a single annotator. This explains patterns of multiple annotation that can be found in the csv version of the dataset, where some articles are coded by over 20 annotators, a group by 2, and many by a single annotator. In the final TEI XML version, however, multiple annotations are not present. The final annotations were derived from whichever annotation found the most mentions in an article, then processed through iterative refinement (as described tersely above and, with comment, below).

About half-way through the annotation process students within the group were invited to create a "dashboard" of annotation progress, showing graphs of articles annotated, broken down by annotator. While useful for identifying assigned but not completed work, the dashboard when shown to the group revealed differences in numbers of articles annotated, raising questions of productivity (even after adjusting for page lengths). Judging this potentially problematic, the dashboard was kept in the source code, but not further used.

## Assessing agreement

After the bulk of annotator training and a period of annotators dual coding articles we sought to assess annotator agreement. That required aligning the `full_quote` fields being produced by annotators with the PMC XML. That process was more difficult than expected, taking the PI around three weeks. During that time annotators continued to work, as they were "contracted" (as it were) for 10 hours a week.

More on XML full quote matching?

Show stats.

These stats were presented to the group (although not all annotators were present) and discussed. This brought a number of questions that annotators had to the fore, resulting in a small number of clarifications to the coding scheme, as well as identifying a number of "misses" that reflecting annotators ascribed to fatigue rather than conceptual confusion.

At this point, the PI and team had to decide how to proceed. Literature and industry press was discussing the "image-net" moment, highlighting the surprising importance of large datasets. Agreement levels were at arguably acceptable levels for content analysis, and confidence was high that the discussion had resolved remaining issues (and that fatigue issues were somewhat unavoidable, even with double annotation). Costs were mounting and some trained student annotators were approaching graduation. These reasons combined to inform the decision to switch to single annotators, going forward.

Around this time annotators, in face to face and email discussion, identified two patterns in the work they were doing. The first was that some papers were "monsters" with over 100 mentions. They questioned the value of such repetition and identified those papers as very tiring to work on. The PI and team decided that while packages might be repeated, each provided slightly different context and might be useful. Ultimately we assured the annotators that these had value.

The second pattern identified by annotators discussing their work was the tendency of mentions to "cluster" within a paper, occurring more densely in some parts, and less densely in others. Some students, seemingly with natural science backgrounds, suggested these were the "methods and materials" sections, but inspection suggested multiple clusters in different parts of papers. We created an analysis to document this, displaying the clustering to the group. We may follow this up in future research.

We mention these two events because they credibly might have affected annotators work. For example, it is possible that discussing and displaying cluster gave annotators reason to concentrate in some sections but skim others. Similarly, we mention the "monster" papers because annotation patterns may be different in those, particularly towards the end of the fatiguing and repetitious articles. We have not investigated whether annotations differ in these "monster" articles, or before and after group discussion of clustering (although we hope a community might be inspired to do so).

- Connection with GROBID creator and ML expert.
    - Alignment via GROBID
    - Prototype machine learning
    - Annotation consistency work
        - undermining the "software_used" category.
        - not applied to articles with no initial mentions.
        - point to github issues, although discussion frequently reverted to email.
    - Agreement round 2.
    - Binding TEI XML back to provenance, interdisciplinary shear there.



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
