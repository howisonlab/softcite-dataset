# Softcite XML Corpus files

The corpus follows the [TEI XML encoding standard](https://tei-c.org/) with a corpus level decription (`<teiCorpus>`) and an article-level description (`<TEI>`). We provide the full paragraph context for every annotations. Possible attributes of a softare mention (`version`, `url`, `publisher`) are associated to the `@xml:id` of the software name via a `@corresp` XML pointer attribute. 

The following "gold" versions of the corpus are available:

- `softcite_corpus-compact.tei.xml` contains one TEI entry per article having at least one annotation (total of 1228 articles)

- `softcite_corpus-full.tei.xml` contains one TEI entry per article including those without any annotations (total of 4971 articles)

In this context, "gold" means that all the encoded information have been curated by an expert annotator in addition to a first round of annotation. 

The following "silver" version of the corpus includes some information not double checked by a curator and text segments that could not be aligned automatically with a full paragraph - this is an intermediary version and we expect to finalize the review of all the information in a near future:

- `softcite_corpus-full-silver.tei.xml` contains one TEI entry per article including those without any annotations (total of 4971 articles)

For convenience, the following files contains article entries by collection, PubMed Central (`pmc`) and Economics (`econ`):

- `softcite_corpus_pmc-compact.tei.xml`

- `softcite_corpus_econ-compact.tei.xml`

Finally the file `ids.csv` contains a mapping of all available article identifiers (`DOI`, `PMID`, `PMCID`) with the uniform hexadecimal code used as `@xml:id` for each article. 
