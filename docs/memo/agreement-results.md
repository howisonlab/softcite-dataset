# Agreement Results and Where to Find them
_by Caifan Du_
_on April 2, 2020_

## Data Sources

- First round agreement results (before alignment improvement): See [issue #538](https://github.com/howisonlab/softcite-dataset/issues/538)
- Second round annotation-level agreement (after alignment improvement): See the [linked email copy on Mar 11, 2020](https://github.com/howisonlab/softcite-dataset/blob/master/docs/memo/agreement-after-alignment-improvements_2020-03-11.pdf)
- Selection agreement in PMC article set: See [James's scripts](https://github.com/howisonlab/softcite-dataset/blob/master/code/locateFullQuotesInPDF.Rmd)

## Comparison before & after alignment improvements
1st round agreement in PMC & Econ articles | 2nd round agreement in PMC articles
:--------------------------------------------|:--------------------------------------------:
![](https://raw.githubusercontent.com/caifand/softcite-dataset/master/docs/memo/agreement1_all.png)|![](https://raw.githubusercontent.com/caifand/softcite-dataset/master/docs/memo/agreement2_PMC.png)

1st round agreement in econ articles | 2nd round agreement in econ articles
:--------------------------------------|:--------------------------------------:
![](https://raw.githubusercontent.com/caifand/softcite-dataset/master/docs/memo/agreement1_econ.png)|![](https://raw.githubusercontent.com/caifand/softcite-dataset/master/docs/memo/agreement2_econ.png)

## Agreement of text selection in PMC particles
Calculate the percentage agreement of full_quote in each article, then average the agreement per article out over all the multiply annotated PMC articles.
Overall percentage agreement: 65.42% 
