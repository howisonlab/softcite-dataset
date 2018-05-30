#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
library(tidyverse)
library(data.world)

  ## Database address
softcite_ds = "https://data.world/jameshowison/software-citations/"

  ## Queries
  ## TO-DO - some of these queries could likely be combined to improve perfomance
prefixes <- "
PREFIX bioj: <http://james.howison.name/ontologies/bio-journal-sample#>
PREFIX bioj-cited: <http://james.howison.name/ontologies/bio-journal-sample-citation#>
PREFIX ca: <http://floss.syr.edu/ontologies/2008/4/contentAnalysis.owl#>
PREFIX citec: <http://james.howison.name/ontologies/software-citation-coding#> 
PREFIX dc: <http://dublincore.org/documents/2012/06/14/dcmi-terms/>
PREFIX doap: <http://usefulinc.com/ns/doap#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX vivo: <http://vivoweb.org/ontology/core#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"

softcite_ds = "https://data.world/jameshowison/software-citations/"
mention_query <- data.world::qry_sparql(paste(prefixes,
"SELECT ?article ?coder ?selection ?full_quote ?on_pdf_page ?spans_pages
WHERE { ?article citec:has_in_text_mention ?selection .
?selection ca:isTargetOf
[ rdf:type ca:CodeApplication ;
ca:hasCoder ?coder ;
ca:appliesCode [ rdf:type citec:mention_type ]
] .
?selection citec:full_quote ?full_quote ;
citec:on_pdf_page ?on_pdf_page ;
citec:spans_pages ?spans_pages
}"
))
no_selection_query <- data.world::qry_sparql(paste(prefixes,
"SELECT ?article ?coder 
WHERE { ?article ca:isTargetOf
[ rdf:type ca:CodeApplication ;
ca:hasCoder ?coder ;
ca:appliesCode [ rdf:type citec:coded_no_in_text_mentions ;
citec:isPresent true ]
]
}"
))
software_name_query <- data.world::qry_sparql(paste(prefixes,
"SELECT ?software_name
WHERE {
?article citec:has_in_text_mention ?selection .
?selection ca:isTargetOf
[ rdf:type ca:CodeApplication ;
ca:appliesCode [ rdf:type citec:software_name ;
rdfs:label ?software_name ;
citec:isPresent true ] ;
ca:hasCoder ?coder ]
}"
))
has_name_query <- data.world::qry_sparql(paste(prefixes,
"SELECT ?has_software_name
WHERE {
?article citec:has_in_text_mention ?selection .
?selection ca:isTargetOf
[ rdf:type ca:CodeApplication ;
ca:appliesCode [ rdf:type citec:software_name ;
citec:isPresent ?has_software_name ] ;
ca:hasCoder ?coder ]
}"
))
has_version_query <- data.world::qry_sparql(paste(prefixes,
"SELECT ?has_version_num
WHERE {
?article citec:has_in_text_mention ?selection .
?selection ca:isTargetOf
[ rdf:type ca:CodeApplication ;
ca:appliesCode [ rdf:type citec:version_number ;
citec:isPresent ?has_version_num ] ;
ca:hasCoder ?coder ]
}"
))
has_url_query <- data.world::qry_sparql(paste(prefixes,
"SELECT ?has_url
WHERE {
?article citec:has_in_text_mention ?selection .
?selection ca:isTargetOf
[ rdf:type ca:CodeApplication ;
ca:appliesCode [ rdf:type citec:url ;
citec:isPresent ?has_url ] ;
ca:hasCoder ?coder ]
}"
))



  ## data.world queries

mentions <- data.world::query(mention_query, softcite_ds) %>% 
  as.tibble(mentions) %>% 
  filter(str_detect(article, "PMC")) %>% 
  mutate_at(vars(article, selection),
            funs(str_extract(.,"[#/]([^#/]+)$"))) %>%
  mutate_at(vars(article,selection), funs(str_sub(.,2)))

found_selections <- mentions %>% 
  select(article, coder) %>% 
  distinct()

no_selection_articles <- data.world::query(no_selection_query, softcite_ds) %>% 
  mutate(article = str_extract(article, "[#/]([^#/]+)$"),
         article = str_sub(article,2),
         matched = 0,
         unmatched = 0) %>% 
  select(article, coder) %>% 
  collect()

all_coded_articles <- bind_rows(found_selections, no_selection_articles)

software_names <- data.world::query(software_name_query, softcite_ds) %>% 
  as.tibble()
#software_names <- sapply(software_names, tolower)

has_name <- data.world::query(has_name_query, softcite_ds) %>% 
  table()

has_version <- data.world::query(has_version_query, softcite_ds) %>% 
  table()

has_url <- data.world::query(has_url_query, softcite_ds) %>% 
  table()



  ## Methods to access useful stats

getFracNames <- function(){
  with_name <- has_name["true"]
  return(with_name/(with_name+has_name["false"]))
}
getFracVersions <- function(){
  with_version <- has_version["true"]
  return(with_version/(with_version+has_version["false"]))
}
getFracUrls <- function(){
  with_url <- has_url["true"]
  return(with_url/(with_url+has_url["false"]))
}
getNumMentions <- function(){
  return(length(mentions$article))
}
getNumArticles <- function(){
  return(length(unique(all_coded_articles$article)))
  #return(nrow(na.omit(distinct(all_coded_articles)))) #total number of distinct articles
}
getNumCoders <- function(){
  return(length(unique(all_coded_articles$coder)))
}
getSoftwareNames <- function(){
  return(software_names)
}
getMostCommonSoftware <- function(){
  return(sort(table(software_names),decreasing=TRUE)[1:10])
}


  ## Server Logic
  ## Defines output values and visualizations
shinyServer(function(input, output) {
  output$num_articles <- renderValueBox({
      valueBox(
        getNumArticles(), "Unique Articles Analyzed", icon = icon("list-alt", lib = "glyphicon"),
        color = "yellow"
      )
    })
  output$num_coders <- renderValueBox({
    valueBox(
      getNumCoders(), "Contributing Coders", icon = icon("user", lib = "glyphicon"),
      color = "purple"
    )
  })
  output$num_mentions <- renderValueBox({
    valueBox(
      getNumMentions(), "Software Mentions Found", icon = icon("ok",lib = "glyphicon"),
      color = "blue"
    )
  })
  
  #Barplot descibing aspects of mentions
  #Would this look better as multiple pie plots??
  output$mention_compositions <- renderPlot({
    data <- c(getFracNames(), getFracVersions(), getFracUrls())
    par(mar=c(5,8,4,2)) # increase y-axis margin.
    barplot(data, names.arg=c("Software\nName", "Version\nNumber", "URL"),
            xlab = "Mention Characteristic",
            ylab = "Fraction of Total Mentions with Characteristic")
  })
  
  #Barplot of 10 most common software names
  output$software_names_chart <- renderPlot({
    data <- getMostCommonSoftware()
    par(las=2) # make label text perpendicular to axis
    par(mar=c(5,8,4,2)) # increase y-axis margin.
    barplot(data, horiz = TRUE,
            xlab = "Amount of References")
            #ylab = "Software Name")
  })
  
})
