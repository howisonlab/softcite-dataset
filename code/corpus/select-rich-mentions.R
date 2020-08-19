# August 17, 2020. Mon

# Selecting software mentions in Softcite TEI/XML corpus

library(tidyverse)
library(xml2)
library(here)

tei_doc <- read_xml("https://raw.githubusercontent.com/howisonlab/softcite-dataset/master/data/corpus/softcite_corpus-full.tei.xml") %>% xml_ns_strip()

# Auditing corpus annotations
n_software <- xml_find_num(tei_doc, xpath="count(//rs[@type='software'])")
n_attrs <- xml_find_num(tei_doc, xpath="count(//rs[not(@type='software')])")
n_anno <- xml_find_num(tei_doc, xpath="count(//rs)")
n_article <- xml_find_num(tei_doc, xpath="count(//fileDesc[@xml:id])")
n_article_zero_mention <- xml_find_num(tei_doc, xpath="count(//body[not(node())])")
n_biom_article <- xml_find_num(tei_doc, xpath="count(//TEI[@subtype='pmc'])")
n_econ_article <- xml_find_num(tei_doc, xpath="count(//TEI[@subtype='econ'])")

dbl_coded <- xml_find_num(tei_doc, xpath="count(//textClass/catRef[@target='#multiple_annotator'])")
coded_once <- xml_find_num(tei_doc, xpath="count(//textClass/catRef[@target='#unique_annotator'])")

n_sw_used <- xml_find_num(tei_doc, xpath="count(//rs[@subtype='used'])")
n_sw_used_econ <- xml_find_num(tei_doc, xpath="count(//TEI[@subtype='econ']//rs[@subtype='used'])")
n_sw_econ <- xml_find_num(tei_doc, xpath="count(//TEI[@subtype='econ']//rs[@type='software'])")

n_publisher <- xml_find_num(tei_doc, xpath="count(//rs[@type='publisher'])")
n_version <- xml_find_num(tei_doc, xpath="count(//rs[@type='version'])")
n_url <- xml_find_num(tei_doc, xpath="count(//rs[@type='url'])")

corpus_stats <- tibble(n_software, n_attrs, n_anno, n_article, n_article_zero_mention, n_biom_article, n_econ_article, dbl_coded, coded_once, n_sw_used, n_sw_used_econ, n_sw_econ, n_publisher, n_version, n_url)
# write to data/corpus-stats.csv

# how software are mentioned
rs_software <- tei_doc %>% 
  xml_find_all(xpath="//rs[@type='software']") 
# 5171 software mentions in total
software_in_p <- tei_doc %>% 
  xml_find_all(xpath="//p/rs[@type='software']")
# 4091 software mentions in p

software_p <- tibble(rs_txt = xml_text(software_in_p), rs_attrs = xml_attrs(software_in_p)) %>% 
  unnest_wider(rs_attrs) %>% 
  rename(software = rs_txt)

software_id <- software_p %>% pull(id)

# remember to check if an software mention is attached with more than publisher, url, or version
rs_publisher <- tei_doc %>% 
  xml_find_all(xpath="//rs[@type='publisher']")
# 1358 publisher mentions
publisher_in_p <- tei_doc %>% 
  xml_find_all(xpath="//p/rs[@type='publisher']")
# among which 1111 publisher mentions in </p>

publisher_p <- tibble(rs_txt = xml_text(publisher_in_p), 
                    rs_attrs = xml_attrs(publisher_in_p)) %>% 
  unnest_wider(rs_attrs) %>% 
  mutate(corresp = str_sub(corresp, 2, -1)) %>% 
  rename(id = corresp, publisher=rs_txt) %>% 
  select(publisher, id) %>% 
  group_by(id) %>% 
  mutate(row = row_number()) %>% 
  pivot_wider(names_from = row, values_from = publisher) %>% 
  rename(publisher1=`1`, publisher2=`2`) %>% ungroup()

publisher_p %>% filter(!is.na(publisher2))

rs_url <- tei_doc %>% 
  xml_find_all(xpath="//rs[@type='url']") 
# 215 url mentions
url_in_p <- tei_doc %>% 
  xml_find_all(xpath="//p/rs[@type='url']")
# 172 url mentions in </p>

url_p <- tibble(rs_txt = xml_text(url_in_p), 
              rs_attrs = xml_attrs(url_in_p)) %>% 
  unnest_wider(rs_attrs) %>% 
  mutate(corresp = str_sub(corresp, 2, -1)) %>% 
  rename(id = corresp, url = rs_txt) %>% 
  select(url, id)

rs_version <- tei_doc %>% 
  xml_find_all(xpath="//rs[@type='version']")
# 1591 version mentions
version_in_p <- tei_doc %>% 
  xml_find_all(xpath="//p/rs[@type='version']")
# 1258 version mentions in </p>

version_p <- tibble(rs_txt = xml_text(version_in_p), 
                  rs_attrs = xml_attrs(version_in_p)) %>% 
  unnest_wider(rs_attrs) %>% 
  mutate(corresp = str_sub(corresp, 2, -1)) %>%
  rename(id = corresp, version = rs_txt) %>% 
  select(version, id) %>% 
  group_by(id) %>% 
  mutate(row = row_number()) %>% 
  pivot_wider(names_from = row, values_from = version) %>% 
  rename(version1=`1`, version2=`2`) %>% ungroup()

version_p %>% filter(!is.na(version2))

pmc_id <- tei_doc %>% 
  xml_find_all(xpath="//TEI[@subtype='pmc']//fileDesc") %>% 
  xml_attrs %>% unlist

# rectangular data of annotated software mentions in </p> parsed from TEI corpus
mentions_p <- software_p %>% left_join(version_p, by="id") %>% 
  left_join(publisher_p, by="id") %>% 
  left_join(url_p, by="id") %>% 
  mutate(article = str_extract(id, "[A-Za-z0-9]{10}")) %>% 
  mutate(article_set = 
           if_else(article %in% pmc_id, "PMC", "Economics")) 

# Selecting rich mentions
all_mentioned <- mentions_p %>% 
  filter(!is.na(version1) & !is.na(publisher1) & !is.na(url)) %>% 
  # 9 software mentioned with everything
  mutate(mention_status = "all") %>% 
  filter(article_set == "PMC")
  # 9 software mentions in PMC article set with every detail

sw_ver_pub <- mentions_p %>% 
  filter(!is.na(version1) & !is.na(publisher1)) %>% 
# 699 software mentioned with version and publisher together in PMC articles
  mutate(mention_status = "sw-ver-pub") 

sw_ver_url <- mentions_p %>% 
  filter(!is.na(version1) & !is.na(url)) %>% 
# 36 software mentioned with version and URL in PMC articles
  mutate(mention_status = "sw-ver-url")

sw_pub_url <- mentions_p %>% 
  filter(!is.na(publisher1) & !is.na(url)) %>% 
# 20 software mentioned with publisher and URL in PMC articles
  mutate(mention_status = "sw-pub-url") 

add = as.numeric(200-tally(all_mentioned)-30)

mention_sample <- bind_rows(sw_ver_pub, sw_ver_url, sw_pub_url) %>% 
  filter(article_set=="PMC") %>% 
  sample_n(size=add, replace=FALSE) %>% 
  bind_rows(all_mentioned)

library(janitor)
mention_sample %>% 
  tabyl(mention_status)
# write to data/170_mention_sample_tasks.csv
# use annotation `id` to identify text!

