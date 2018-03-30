"""Assign new work to a coder.

1. Script connects to mysql database to get new work assignment (publication)
   - find the next publication that they have not coded.
2. git pull upstream to renew coding scheme
3. use coding scheme and work assignment to create individuals file
4. and place in the right place.  Coders will git status, add, commit.
"""

from getUsername import get_username_from_github
import pymysql
import pprint
import os
import pwd
import re
import csv
import sys
from urllib.parse import quote

"""Given a pub_id and a username, creates appropriate
individuals file, and checks it into github."""
def generate_template_file(pub_id, username):
    # create appropriate file
    make_sure_path_exists("data/individuals-{}".format(username))
    filename = "data/individuals-{}/{}-econ-{}.ttl".format(username, username, pub_id)
    header = """
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .

@prefix ca: <http://floss.syr.edu/ontologies/2008/4/contentAnalysis.owl#> .
@prefix doap: <http://usefulinc.com/ns/doap#> .
@prefix vivo: <http://vivoweb.org/ontology/core#> .

@prefix bioj: <http://james.howison.name/ontologies/bio-journal-sample#> .
@prefix citec: <http://james.howison.name/ontologies/software-citation-coding#> .
@prefix bioj-cited: <http://james.howison.name/ontologies/bio-journal-sample-citation#> .
@prefix pmcid: <https://www.ncbi.nlm.nih.gov/pmc/articles/> .
@prefix pmcid-cited: <http://james.howison.name/ontologies/pmcid-journal-sample-citation#> .
@prefix doi: <http://doi.org/> .
@prefix doi-cited: <http://james.howison.name/ontologies/doi-journal-sample-citation#> .

@prefix dc: <http://dublincore.org/documents/2012/06/14/dcmi-terms/> .

# https://github.com/howisonlab/softcite-pdf-files/blob/master/docs/pdf-files/economics_pdf_files/{doi_encoded}.pdf
# also https://doi.org/{doi}
doi:{doi} rdf:type bioj:article ;
    rdf:type bioj:econ_article ;

    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "{username}" ;
          ca:appliesCode [ rdf:type citec:codable ;
                           citec:isPresent FIXME; # true if can code
                         ] ;
        ] ;

    ca:isTargetOf
        [ rdf:type ca:CodeApplication ;
          ca:hasCoder "{username}" ;
          ca:appliesCode [ rdf:type citec:coded_no_in_text_mentions ;
                           citec:isPresent FIXME; # true/false
                         ] ;
        ] ;


    citec:has_in_text_mention FIXME ;
    # create name for in_text_mention like
    # doi:{doi}_JH01

    # citations like:
    # doi-cited:{doi}_AuthorYear
.
"""
    content = header.format(doi = pub_id, username = username, doi_encoded = quote(pub_id))

    ttl_file = open(filename, "x")
    ttl_file.write(content)
    ttl_file.close()

    print("Created {}".format(filename))
    print("You may need to right click and refresh your folder in Atom.")


"""Returns a new task for a coder, altering the database"""
def get_new_task(conn, coder):
    conn.execute("""LOCK TABLE assignments WRITE,
                               assignments AS ass_read READ""")

    # Currently just avoids having both of that pub
    # assigned to same coder.
    # Future work to balance across pairs needed here.
    get_assignment = """
    SELECT id as task_id, pub_id
    FROM assignments
    WHERE assigned = FALSE
      AND pub_id NOT IN ( -- Checks that that pub isn't already ass
                            SELECT pub_id
                            FROM assignments AS ass_read
                            WHERE ass_read.assigned_to = %(coder)s
      )
    ORDER BY id ASC
    LIMIT 1
    """
    conn.execute(get_assignment, {"coder": coder})

    result = conn.fetchone()

    try:
        new_task_id = result["task_id"]
    except TypeError:
        print("TypeError finding new tasks, "
              "no tasks in queue?")
        exit()

    set_assignment = """
    UPDATE assignments
    SET assigned = TRUE,
        assigned_to = %(coder)s,
        asssigned_timestamp = NOW()
    WHERE id = %(task_id)s
    """
    param_dict = {"coder": coder, "task_id": new_task_id}
    conn.execute(set_assignment, param_dict)

    check_assign = """
    SELECT * FROM assignments WHERE id = %(task_id)s"""
    conn.execute(check_assign, {"task_id": result["task_id"]})
    post_result = conn.fetchone()
    # print(post_result)

    return post_result["pub_id"]

    conn.execute("UNLOCK TABLES")

def create_database(cursor):
    sql = """
CREATE TABLE assignments (
    id INT AUTO_INCREMENT,    -- primary key
    pub_id VARCHAR(255) NOT NULL,  -- doubled
    random_order INT UNIQUE NOT NULL,      -- unique
    assigned BOOLEAN NOT NULL DEFAULT False,      --
    assigned_to VARCHAR(24), -- NULL
    asssigned_timestamp DATETIME,
    PRIMARY KEY (id)
)
    """
# GRANT ALL PRIVILEGES
# ON softcite_assignments.*
# TO 'softcite_user'@'localhost'
# IDENTIFIED BY 'work_spree34'
# WITH GRANT OPTION;

    cursor.execute(sql)

"""Insert PMC tasks.

These are read from oa_shuffled_with_header.csv which is randomized. It was randomized on 21 June 2017 using:
tail -n +2 oa_file_list.csv | gshuf > oa_list_shuffled.csv
This method checks how many PMC tasks are there and skips that many lines from the input, to avoid adding duplicates.
"""
def insert_pmc_tasks(filename, conn):
    #filename = "data/pmc_oa_dataset/oa_shuffled_with_header.csv"
    # headers:
    # File,Article Citation,Accession ID,Last Updated (YYYY-MM-DD HH:MM:SS),PMID,License
    with open(filename) as csvfile:
        myCSVReader = csv.DictReader(csvfile,
                                    delimiter=",",
                                    quotechar='"')
        pubs_to_code = []
        for row in myCSVReader:
            file_list.append(row["Accession ID"])

        doubled_list = [x for item in pubs_to_code for x in repeat(item, 2)]

        for order, task in enumerate(doubled_list):
            print(order + task)
            # insert_task(conn, order, task)

"""Read all pub numbers from pubInfoDataSet.ttl."""
def get_pubs_to_code():
    import rdflib
    import glob

    g = rdflib.Graph()
    g.parse("data/publications_sets.ttl", format="n3")

    # for file_to_check in glob.iglob("data/individuals-hannah/*.ttl"):
    #     print(file_to_check)
    #     g.parse(file_to_check, format="n3")
    #
    # for file_to_check in glob.iglob("data/individuals-james/*.ttl"):
    #     print(file_to_check)
    #     g.parse(file_to_check, format="n3")
    #
    # for file_to_check in glob.iglob("data/agreement*.ttl"):
    #     print(file_to_check)
    #     g.parse(file_to_check, format="n3")

    sparql_query_all = """
    SELECT DISTINCT ?pub_id
    WHERE {
       bioj:agreement2 ca:set_includes ?pub_id
          }
    """

    qres = g.query(sparql_query_all)
    pub_list = []

    for row in qres:
        matches = re.search('#a(.*?)$', row.pub_id)
        local_part = matches.group(1)
        pub_list.append(local_part)
    print(len(pub_list))

    # Remove already assigned.
    # sparql_query_assigned = """
    # SELECT DISTINCT ?pub_id
    # WHERE {
    #    ?pub_id rdf:type bioj:article ;
    #              ca:isTargetOf ?code_app .
    #    ?code_app ca:appliesCode ?code .
    #    ?code rdf:type transition:intendsToCreateSoftware .
    #       }
    # """
    # qres = g.query(sparql_query_assigned)
    # pub_list_applied = []
    # for row in qres:
    #     pub_list_applied.append(row.pub_id[-5:])
    #
    # print(len(pub_list_applied))
    #
    # pub_list = set(pub_list) - set(pub_list_applied)
    #
    # print(len(pub_list))
    #
    return list(pub_list)


def randomize_and_insert(conn):
    from random import shuffle
    from itertools import repeat

    pubs_to_code = get_pubs_to_code()
    shuffle(pubs_to_code)

    # [10,23] ==> [10,10,23,23]
    doubled_list = [x for item in pubs_to_code for x in repeat(item, 11)]

    for order, task in enumerate(doubled_list):
        insert_task(conn, order, task)

def insert_task(conn, order, task):
    insert_sql = """INSERT INTO assignments(pub_id, random_order)
                         VALUE (%(task)s, %(order)s)
                 """
    conn.execute(insert_sql, {"task": task, "order": order})
    print("Inserted {}".format(task))

import os
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

"""def get_username_from_github():
    import subprocess
    import re

    remotes_string = subprocess.check_output(
            ["git", "remote", "-v"]
    ).decode("utf8")
    # print(remotes_string)
    # remotes_list = remotes_string.split()
    # remote = remotes_list[1]
    # print(remote)
    # origin	git@github.com:howisonlab/softcite-dataset.git (fetch)
    matches = re.search('origin.*?github.com.(.*?)/softcite-dataset', remotes_string)
    username = matches.group(1)
    if (username == "howisonlab"):
        username = "jameshowison"

    return username.lower()"""

if __name__ == '__main__':

    connection = pymysql.connect(host="localhost",
                                 user="softcite_user",
                                 passwd="work_spree34",
                                 db="softcite_assignments",
                                 autocommit=True,
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    # cursor.execute("TRUNCATE assignments")

    # print(get_pubs_to_code())
    # create_database(cursor)
    # randomize_and_insert(cursor)
    # insert_pmc_tasks(sys.argv[1], connection)
    # This will fail unless on linux, should be run on
    # howisonlab anyway.

    # Check that script is run from right location.
    neededPath = "code/getNextContentAnalysisAssignment.py"
    if (sys.argv[0] != neededPath):
        raise Exception("Must run script from ~/transition")

    try:
        username = get_username_from_github()
        # username = sys.argv[1]
        print("Got username '{}'".format(username))
    except IndexError:
        raise Exception("Must pass github username as argument")

    # # print(username)
    # # username = pwd.getpwuid(os.getuid()).pw_name
    # # username = "tester"
    pub_id = get_new_task(cursor, username)
    generate_template_file(pub_id, username)
