"""generate markdown from coding-scheme.ttl"""

# Usage: python3 code/generate_coding_scheme_html.py > docs/coding-scheme.html

import rdflib
import pprint
import re
import sys
import datetime
import pytz
from tzlocal import get_localzone
import glob
import tabulate

g = rdflib.Graph()
g.parse("data/softcite-coding-scheme.ttl", format="n3")

def get_list(g):

    sparql_query = """
    SELECT ?code ?round ?order ?comment ?example
    WHERE {{
        ?code ca:codingOrder ?order ;
              ca:codingRound ?round ;
              rdfs:comment ?comment ;
              ca:example ?example .

    }} ORDER BY ASC(?round) ASC(?order)
    """
    # MAKING EXAMPLE OPTIONAL IS A PAIN; JUST ADD AN EXAMPLE TO ALL CODES
    #sparql_query = sparql_query.format(codingRound)

    # print(sparql_query)

    qres = g.query(sparql_query)

    output = []
    for result in qres:

        output.append([result.code.n3(g.namespace_manager)[6:], # citec:
                      result.comment.toPython().replace("\n","\n<br />"),
                      result.example.toPython().replace("\n","\n<br />")
                      ])
#have a function that calls the relevant code for phase 1, 2, 3 and then place that content appropriately

    print(tabulate.tabulate(output,
      headers = ["Code", "Comment", "Example"],
      tablefmt="html")
      )
    # for result in qres:
    #     templateContents += template.format(coder,
    #                                     result.code.n3(g.namespace_manager),
    #                                     result.template.toPython()
    #                                     )
    #
    # return templateContents
# Code below calls the function above.


if __name__ == '__main__':

    print("""
<html lang="en">
<head>
	<meta charset="utf-8" />
	<title>Table Style</title>
	<meta name="viewport" content="initial-scale=1.0; maximum-scale=1.0; width=device-width;">
    <link rel="stylesheet" type="text/css" href="data-table.css">
</head>
""")
    print("<h1>Coding Scheme</h1>")

    get_list(g)

    print("</html>")
