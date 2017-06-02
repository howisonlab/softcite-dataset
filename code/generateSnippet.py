"""generate snippet from coding-scheme.ttl.
Usage: python3 code/generateSnippet.py <github_user_name> > my_snippet
"""

import rdflib
import pprint
import re
import sys
import datetime
import pytz
from tzlocal import get_localzone
import glob

coder = sys.argv[1]
# don't need this if you are making it into a function
# and providing the coding round

g = rdflib.Graph()
g.parse("data/softcite-coding-scheme.ttl", format="n3")

def get_template_for_scope(g, scope):

    sparql_query = """
    SELECT ?code ?template
    WHERE {{
        ?code ca:codingOrder ?order ;
              ca:scope "{}" .
        OPTIONAL {{?code ca:template ?template}}
    }} ORDER BY ASC(?order)
    """

    sparql_query = sparql_query.format(scope)

    print(sparql_query)

    qres = g.query(sparql_query)

# header = """
# '.source.turtle':
#   'All Transition Codes':
#     'prefix': 'trans'
#     'body': \"\"\""""
#
# print(header)

    template = """
                    ca:isTargetOf
                        [ rdf:type ca:CodeApplication ;
                          ca:hasCoder "{}" ;
                          ca:codedAt "FIXME"^^xsd:dateTime ;
                          ca:appliesCode [ rdf:type {} ;
                                           {}
                                         ] ;
                        ] ;"""

#have a function that calls the relevant code for phase 1, 2, 3 and then place that content appropriately

    templateContents = ""

    for result in qres:
        templateContents += template.format(coder,
                        result.code.n3(g.namespace_manager),
                        result.template.toPython()
                        )

    return templateContents
# Code below calls the function above.
if __name__ == '__main__':

    completeTemplate = """
    '.source.turtle':
      'true':
        'prefix': 'tr'
        'body': 'true'
      'false':
        'prefix': 'fa'
        'body': 'false'
      'comment':
        'prefix': 'ca'
        'body': 'ca:comment """ """'
      'url':
        'prefix': 'url'
        'body': \"\"\"<FIXME> rdf:type transition:projectURL ;

                      .\"\"\"
      'memo':
        'prefix': 'mem'
        'body': 'ca:memo """ """'
      'has_supplement':
        'prefix': 'hs'
        'body': 'citec:has_supplement [ rdf:type citec:supplement ;
                           citec:isPresent FIXME ] ;'
      'has_in_text_mention':
       'prefix': 'hitm'
       'body': 'citec:has_in_text_mention bioj:FIXME ;'
      'article block':
        'prefix': 'artb'
        'body': \"\"\"
                    {}\"\"\"
      'in-text block':
         'prefix': 'itb'
         'body': \"\"\"
                    {}\"\"\"
      'reference block':
         'prefix': 'refb'
         'body': \"\"\"
                    {}\"\"\"
    """

    article_string = get_template_for_scope(g, "article")
    in_text_mention_string = get_template_for_scope(g, "in-text_mention") + get_template_for_scope(g, "both")
    reference_string = get_template_for_scope(g, "reference") + get_template_for_scope(g, "both")


    outputString = completeTemplate.format(article_string,
                            in_text_mention_string,
                            reference_string
                            )

    print(outputString)
