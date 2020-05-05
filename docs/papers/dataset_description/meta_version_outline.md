Motivation and Prior Work

Researchers and industry are increasing labeling (or annotating) data to facilitate machine learning. Drawing on and adapting qualitative content analysis techniques. Little formalized guidance available. Data annotation is also rediscovering some challenges of data provenance familiar to the information sciences.

The goal of this paper is thus two-fold: to present a labeled dataset, and to reflect on the process and challenges in its creation and presentation. To meet this goal we present three parts. The first is a paper within a paper, straightforwardly describing our annotation project. The second provides substantial process and provenance description (including mis-steps and detailed decisions). The third reflects on the overall process, describing tensions experienced and highlighting areas where information science can provide further guidance for supervised machine learning dataset creation projects.

1. Genre paper: a gold standard dataset on software mentions in the scientific literature
    - Motivation and prior work on entity extraction
        - Software visibility
        - Entity extraction
        - Bootstrapping and recall
        - Particularly full text challenges and running at scale
    - TEI XML file & format
    - Final coding scheme and agreement figures (appendix published on Zotero)
    - Summary of annotations
    - Use and improvement in an ML system
    - Future work
        - CiteAs/Software Impact Story plans
        - Shared annotation project

2. Provenance Presentation
    - Starts with process figure (consider a little more timeline?)
    - Genesis of the project (from Howison and Bullard), includes origin of the "software used" category and connection with formalized citation (explains some choices?)
    - Choice of papers to code. PubMed Open access Driven by availability of XML, and open access for eventual open publication.
    - Collaboration infrastructure.
        - Why github?
        - Format of the annotations (RDF).
    - Recruitment and training of students.  Using the papers from the Howison and Bullard dataset. Training materials on github.
    - Paper provision, limiting number.  Still ended up with quite high imbalance.
        - Creation of "dashboard"
    - Agreement assessment, round 1.
        - Alignment, pre-GROBID.
        - Identification of mention "clustering"
    - Choice to switch to single coding
        - influenced by belief in size of data, frustration at slowness.
        - How many coded in this period?
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
        - opens up criticism??  For example, while writing section 2, we wrestled with whether and how to discuss missed double coded articles. Simple typo, or issue that others would need to know?  Same with "dashboard" and "clustering" analyses, unclear whether these are worth presenting, hard to reason about whether/how they might have mattered.
        - Some interdisciplinary friction here, as well.
    - Presenting dataset as artifact vs process
        - genre expectations
        - hard to know how much to describe (cite Ribes article, but also cite data sharing literature)
        - Documenting the work of annotators, including their frustrations and practices, seems a crucial source of provenance, but quite outside the usual expectations.
    - Openness vs fear of being scooped
    - involving non-students for pay is complicated, perhaps better to offer transfer credit.
