# Curation Rules
_December 18, 2020_

v1.0

We applied these rules to the first release of the Softcite corpus in order to ensure annotation consistency.

For history records, see:
https://github.com/howisonlab/softcite-dataset/issues/637 
https://github.com/howisonlab/softcite-dataset/issues/638

1. The annotation of `version` only includes the software version number, name, or data, without any other token such as "version", "v.", "ver.", or punctuations.

2. The annotation of software `publisher` only includes the name of the individual(s) or organization(s) that creates/publishes the software. Do not include individual affiliation or organizational geo-location information into the annotation. For names of business entities include the types if present in the text (e.g., Inc., GmbH, etc.).

3. Programming languages are software. We annotate them when they are mentioned as the environment or framework where a piece of software was implemented.

4. We always include the acronym into the annotation of `software` names when they are closely put together in the text. If they occur in different places, we annotate them as separate software mentions. Currently software names are always considered as a continuous chunk. 
```
using the <rs type="software">Ingenuity Pathways Analysis (IPA)</rs> tool <ref type="figure">(Figure 3</ref>b). 
The user interface was linked to a <rs type="software">My Structured Query Language (MySQL)</rs> database 
```

5. Theoretical/statistical models are not annotated as software.
```
The CGE model we describe in this section is the GTAP6inGAMS model developed by <ref type="bibr">Rutherford (2005)</ref>.
```
The software that is used in the model is called **GAMS**.

6. R packages are annotated as one entity if they are mentioned together:
```
using the <rs type="software">R package proCIs</rs>
```

7. When an operating system is mentioned along with a software, we do not specifically annotate it as a separate piece of software. We consider it as secondary details about a piece of specific software. However, when they are individually mentioned, we annotate them as a software mention.
```
Convertible tablets, for which <rs type="software">Windows</rs> was the dominant operating system, are being overwhelmed by the new popularity of slate tablets.
```

8. We annotate non-named software mentions such as "custom script" or "in-house script".
```
Data analysis and model fitting were performed using <rs type="software">custom scripts</rs> written in <rs id="software-1" type="software">Igor Pro</rs> <rs corresp="#software-1" type="version">6</rs> (<rs corresp="#software-1" type="creator">WaveMetrics</rs>).</p>

Second, since <rs type="software">Matlab</rs> <rs id="software-0" type="software">routines</rs> applying Bayesian methods to the spatial lag, spatial error and spatial ...
```

9. Scientific methods/techniques are not equal to software.
```
Start the <rs type="software">CL</rs> control program
```
In PMC4927739, cathodoluminescence (CL) is a physical reaction used as a measurement method. CL is wrongly annotated as a software in this case. Instead **CL control program** is a software mention where the software is unnamed.

```
Open the <rs type="software">EBSD</rs> control software and load the calibration file for the chosen WD. 8. Set up the measurement in the <rs type="software">EBSD</rs> control software according to the operating manual
```
This one is the same case. EBSD refers to the electron backscatter diffraction technique. The **EBSD control software** is the actual unnamed software mention here.

10. Databases such as UniprotKB or Swissprot, HGMD (Human Gene Mutation Database), miRBase, GenBank, etc. are not software. However, database management software such as **MySQL** is software that should be annotated once mentioned. If it is a platform the supports data processing/analysis functionalities using databases, we annotate it (e.g., HydroShare). If a component of such data processing platforms is mentioned, such as **Ensembl browser**, we annotated it as software.

11. We distinguish software publisher and software name when used in combination. 
```
<rs corresp="#PMC0000000-software-1" type="creator">Microsoft</rs> <rs type="software" xml:id="PMC0000000-software-1">Excel</rs>
```

12. We annotated **GraphPad Prism** and **Lotus Notes** as continuous software names.
