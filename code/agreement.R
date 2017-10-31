# setwd("/Users/howison/Documents/UTexas/Projects/SloanSoftCite/softcite-dataset-howisonlab")
# source("code/agreement.R")

# agreement in the softcite context is:
# percent agreement for selections.  First have to figure out a way to see if the selections are the same.
# In the original publication we did that by manually stating
# JH01 bioj:matches C01.

# We need a better way to do this.
1. Find the coder with the largest number of selections
2. For each other coder compare each to each and see which are the most similar.
3. Pick some threshold?

Similarity methods:
- match on_pdf_page +- 1
- fuzzy string matching on full_quote

This is really clustering using similarity metrics?

# Getting the data (from data.world)
# PREFIX bioj: <http://james.howison.name/ontologies/bio-journal-sample#>
# PREFIX bioj-cited: <http://james.howison.name/ontologies/bio-journal-sample-citation#>
# PREFIX ca: <http://floss.syr.edu/ontologies/2008/4/contentAnalysis.owl#>
# PREFIX citec: <http://james.howison.name/ontologies/software-citation-coding#>
# PREFIX dc: <http://dublincore.org/documents/2012/06/14/dcmi-terms/>
# PREFIX doap: <http://usefulinc.com/ns/doap#>
# PREFIX owl: <http://www.w3.org/2002/07/owl#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX vivo: <http://vivoweb.org/ontology/core#>
# PREFIX xml: <http://www.w3.org/XML/1998/namespace>
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#
# SELECT DISTINCT ?article ?coder ?selection ?quote ?page ?software ?ref
# WHERE {
# 	?article citec:has_in_text_mention ?selection .
# 	?selection citec:full_quote ?quote ;
# 	           citec:on_pdf_page ?page ;
# 	           ca:isTargetOf [ ca:hasCoder ?coder ;
# 	                           ca:appliesCode [ rdf:type citec:software_name ;
# 	                                            citec:isPresent true ;
# 	                                            rdfs:label ?software ]
# 	                          ]
# 	OPTIONAL {?selection citec:has_reference ?ref .}
# }

df <- read.csv("https://query.data.world/s/4z29nsp9kc9lmh5zif8nmjlom",header=T);

# rather ugly code to remove prefixes.
df <- df %>%
       mutate_at(vars(1,3,7),funs(str_extract(.,"#(.*)$"))) %>%
       mutate_at(vars(1,3,7),funs(str_sub(.,2)))

# counts
counts <- df
# Then we were able to use kappa to assess agreement on the codes.  There the unit of coding is the selection, both in-text and references.

library(tidyr)
library(plyr)
library(dplyr)
library(concord)

# convert the URL columns to just local parts.
# df %>% mutate_at(vars(1,3,7),funs(str_extract(.,"#(.*)$"))) %>% mutate_at(vars(1,3,7),funs(str_sub(.,2)))


# url,code,coder,value
agreement <- read.csv("data/agreement-1.csv")

bbc_kappa <- function(data) {
  #print(data)

  unique3 <- unique(data[,3]) # takes all 0s or all 1s down to a single 0 or single 1
  unique4 <- unique(data[,4])

  #kappa.bbc has an issue with if spreadAgree is all 1s or 0s (ie length after unique is 1),
  # this tests for that situation and returns a perfect agreement if found.
  # Note that this is a little problematic, since mostly this means we never saw the code
  # ie. all are zeros.
  if  (length(unique3) == 1 && length(unique4) == 1 && setequal(unique3, unique4)) {
    kappa_bbc = 1
  } else {
    result <- cohen.kappa(data[3:4],"score")
    kappa_bbc = result$kappa.bbc
  }
  return(data.frame("kappa_bbc" = kappa_bbc))
}


#agreement <- read.csv("exported.csv")



spreadAgree <- agreement %>%
                #unite(item, grant, url.coded) %>% # create merged id column
                # change true/false to 1/0
                mutate(value = ifelse(value == "true", 1, 0)) %>%
                # url,code,coder,value
                # move to:
                # url,code,howison,jlcohoon
                # someurl, somecode, 1, 0
                spread(coder,value)

#colnames(spreadAgree) <- c("url","code","coder1","coder2")

# Get codes on intendsToCreateSoftware

# intends <- spreadAgree %>% filter(code=="transition:intendsToCreateSoftware")
#
# intends_bbc <- bbc_kappa(intends)
#
# print("transition:intendsToCreateSoftware agreement:")
# print(intends_bbc)

# Eliminate the grants where either said that intends was false
# false_intends <- spreadAgree %>% filter(code=="transition:intendsToCreateSoftware" & (coder1 == 0 | coder2 == 0))
#
# spreadAgree <- spreadAgree %>% filter(! grant %in% false_intends$grant)
#
# # Remove remaining
# spreadAgree <- spreadAgree %>% filter(! code=="transition:intendsToCreateSoftware")
#
#
# associatedURL <- spreadAgree %>% filter(code=="transition:associatedURL")
#
# associatedURL_bbc <- bbc_kappa(associatedURL)
#
# print("transition:intendassociatedURL agreement:")
# print(associatedURL_bbc)
#
# false_associatedURL <- spreadAgree %>% filter(code=="transition:associatedURL" & (coder1 == 0 | coder2 == 0))
#
# spreadAgree <- spreadAgree %>% filter(! grant %in% false_associatedURL$grant)
#
# spreadAgree <- spreadAgree %>% filter(! code=="transition:associatedURL")

View(spreadAgree)

rows_with_na <- spreadAgree %>% filter(is.na(howison) | is.na(jlcohoon))

print("Found NAs (removed them):")
View(rows_with_na)

spreadAgree <- na.omit(spreadAgree)

# Finally can run agreement on remaining codes
results <- ddply(spreadAgree,.variables="code",.fun=bbc_kappa) %>% arrange(kappa_bbc)

View(results)
