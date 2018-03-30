"""generate snippet from coding-scheme.ttl.
Usage: python3 code/generateSnippet.py <github_user_name> > mySnippet
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

    #print(sparql_query)
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
      'memo':
        'prefix': 'mem'
        'body': 'ca:memo ; # use triple  quotes'
      'in-text block':
         'prefix': 'itb'
         'body': \"\"\"
                        doiFIXME: rdf:type citec:in_text_mention ; # use in text mention name
                            citec:full_quote FIXME ; # use triple quotes

                            citec:on_pdf_page FIXME  ; # integer

                            citec:spans_pages FIXME ; # true/false
                            {}
                            citec:has_reference doi-citedFIXME: ; # name reference like doi-cited:a2004-40-NAT_GENET_Author-YYYY, no quotes
                        .\"\"\"
      'reference block':
         'prefix': 'refb'
         'body': \"\"\"
                        doi-citedFIXME: rdf:type citec:reference ;
                            citec:full_quote FIXME ; # use triple quotes

                            citec:on_pdf_page FIXME  ; # integer

                            citec:spans_pages FIXME ; # true/false
                            {}
                        .\"\"\"
    """

    #article_string = get_template_for_scope(g, "article")
    in_text_mention_string = get_template_for_scope(g, "in-text_mention") + get_template_for_scope(g, "both")
    reference_string = get_template_for_scope(g, "reference") + get_template_for_scope(g, "both")


    outputString = completeTemplate.format(in_text_mention_string,
                            reference_string
                            )

    print(outputString)
