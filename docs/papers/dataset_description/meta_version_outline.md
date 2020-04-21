Motivation and Prior Work

Researchers and industry are increasing labeling (or annotating) data to facilitate machine learning. Drawing on and adapting qualitative content analysis techniques. Little formalized guidance available. Data annotation is also rediscovering some challenges of data provenance familiar to the information sciences.

The goal of this paper is thus two-fold: to present a labeled dataset, and to reflect on the process and challenges in its creation and presentation. To meet  we present three parts. The first is a paper within a paper, straightforwardly describing our annotation project. The second provides substantial process and provenance description (including mis-steps and detailed decisions). The third reflects on the overall process, describing tensions experienced and highlighting areas where information science can provide further guidance for supervised machine learning dataset creation projects.

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
