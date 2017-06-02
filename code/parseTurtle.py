"""Constructs data set."""

import rdflib
import pprint
import sys
import glob
import getopt

def find_all_turtle_files(dir_to_check = "data"):
    files = []
    files += glob.glob(dir_to_check + "*.ttl")
    # Add individuals
    files.extend(glob.glob(dir_to_check + "/individuals-**/*.ttl"))

    return files

def parse_individual_file(file_to_check):
    g = rdflib.Graph()
    result = g.parse(file_to_check, format="n3")
    msg = "{} has {} statements."
    print(msg.format(file_to_check, len(g)))
    return result

def parse_each_file(files):
    for file_to_check in files:
        parse_individual_file(file_to_check)

def build_parse_data_set(dir_to_check = "data"):

    files = find_all_turtle_files(dir_to_check)

    all_files = rdflib.Graph()

    for file_to_check in files:
        print("Parsing {}".format(file_to_check))
        all_files.parse(file_to_check, format="n3")

    return all_files

def build_compiling_data_set(dir_to_check = "data"):

    files = find_all_turtle_files(dir_to_check)

    all_files = rdflib.Graph()

    for file_to_check in files:
        try:
            all_files.parse(file_to_check, format="n3")
        except:
            continue

    return all_files

def usage():
    print("-a to parse all files, -f <filename> for just one file")

def main(argv):
    grammar = "kant.xml"
    try:
        opts, args = getopt.getopt(argv, "af:", ["help", "grammar="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o == "-a":
            build_parse_data_set()
        elif o == "-f":
            parse_individual_file(a)
        else:
            assert False, "unhandled option"

if __name__ == '__main__':
    main(sys.argv[1:])


# sparql_query = """
# SELECT ?grant ?code ?value ?url
# WHERE {
#    ?grant_node rdf:type vivo:grant ;
#                rdfs:label ?grant ;
#              ca:isTargetOf ?ca .
#    ?ca ca:appliesCode ?codeNode .
#    ?codeNode rdf:type ?code .
#    OPTIONAL { ?codeNode transition:isPresent ?value ;
#                          transition:hasURL ?url }
#       }
# """

# sparql_query = """
# SELECT ?grant ?code ?value ?url
# WHERE {
#    ?grant_node rdf:type vivo:grant ;
#                rdfs:label ?grant ;
#              ca:isTargetOf ?ca .
#    ?ca ca:appliesCode [ rdf:type ?code ]
#                         transition:isPresent ?value ;
#                         transition:hasURL ?url ]
#           }
# """# rowDict = {}
 #  rowDict["grant"] = row.grant.n3(g.namespace_manager)
 #  rowDict["code"] = row.code.n3(g.namespace_manager)
 #  rowDict["value"] = row.value.n3(g.namespace_manager)
 #  rowDict["url"] = row.url.n3(g.namespace_manager)
 #  #pprint.pprint(rowDict)
 #  print("{grant},{code},{value},{url}".format(**rowDict))

########
# Full list of codes used.
########

# sparql_query = """
# SELECT DISTINCT ?code
# WHERE {
#    ?ca ca:appliesCode ?codeNode .
#    ?codeNode rdf:type ?code .
#       }
# """
#
# qres = g.query(sparql_query)
#
# for row in qres:
#   print("{} rdf:type transition:ContentAnalysisCode .".format(row.code.n3(g.namespace_manager)))
#
# g = rdflib.Graph()
# result = g.parse("../data/coding-scheme.ttl", format="n3")
#
# print("coding scheme graph has {} statements.".format(len(g)))
#
# sparql_query = """
# SELECT DISTINCT ?code
# WHERE {
#    ?ca ca:appliesCode ?codeNode .
#    ?codeNode rdf:type ?code .
#       }
# """
#
# qres = g.query(sparql_query)
#
# for row in qres:
#   print("{} rdf:type transition:ContentAnalysisCode .".format(row.code.n3(g.namespace_manager)))
