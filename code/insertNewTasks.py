"""Assign new work to a coder.

Inserts new tasks for coders to do.
"""

import pymysql
import pprint
import glob
import os
import pwd
import re
import csv
import sys
from random import shuffle
from itertools import repeat

"""Given a pub_id and a username, creates appropriate
individuals file, and checks it into github."""
def generate_template_file(pub_id, username):
    # create appropriate file
    make_sure_path_exists("data/individuals-{}".format(username))
    filename = "data/individuals-{}/{}-{}.ttl".format(username, username, pub_id)
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
@prefix dc: <http://dublincore.org/documents/2012/06/14/dcmi-terms/> .

# https://howisonlab.github.io/softcite-dataset/pdf-files/{}.pdf
bioj:a{} rdf:type bioj:article ;

    citec:has_supplement [ rdf:type citec:supplement ;
                           citec:isPresent FIXME ] ; # true/false

    citec:has_in_text_mention FIXME ; # name in text mention like bioj:a2004-40-NAT_GENET_JC01, no quotes

    citec:coded_no_in_text_mentions FIXME ; # true/false
.
"""
    content = header.format(pub_id, pub_id)

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

    # store id, give pub_id to student

    set_assignment = """
    UPDATE assignments
    SET assigned = TRUE,
        assigned_to = %(coder)s,
        asssigned_timestamp = NOW()
    WHERE id = %(task_id)s
    """
    param_dict = {"coder": coder, "task_id": result["task_id"]}
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
    random_order INT UNIQUE NOT NULL AUTO_INCREMENT,      -- unique
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

These are read from oa_list_shuffled.csv which is randomized. It was randomized on 21 June 2017 using:
tail -n +2 oa_file_list.csv | gshuf > oa_list_shuffled.csv
This method checks how many PMC tasks are there and skips that many lines from the input, to avoid adding duplicates.
md5sum = 1bd372f619fad53987ab83d2eafa68f0
"""
def insert_pmc_tasks(conn, num_to_insert, coders_per_article=1):
    import os.path
    path = "../softcite-pdf-files/docs/pdf-files/pmc_oa_files/"
    filename = path + "oa_list_shuffled.csv"
    # File,Article Citation,Accession ID,Last Updated (YYYY-MM-DD HH:MM:SS),PMID,License
    with open(filename) as csvfile:
        myCSVReader = csv.DictReader(csvfile,
                                    delimiter=",",
                                    quotechar='"',
                                    fieldnames = ["File","Article Citation","Accession ID","Last Updated (YYYY-MM-DD HH:MM:SS)","PMID","License"])
        pubs_to_code = []
        inserted_count = 0
        for row in myCSVReader:
            if (inserted_count >= num_to_insert):
                break
            print(row)
            print(inserted_count)
            destination = "{}/{}.pdf".format(path, row["Accession ID"])
            if (os.path.exists(destination)):
                continue
            else:
                pmcid_to_insert = row["Accession ID"]
                get_via_ftp(destination, row["File"])

                if (os.path.exists(destination)):
                    write_to_index(row["Article Citation"],
                                   pmcid_to_insert)
                    for task_num in range(0,coders_per_article):
                        insert_task(conn, pmcid_to_insert)
                    inserted_count += 1

        # doubled_list = [x for item in pubs_to_code for x in repeat(item, 2)]

        # for task in doubled_list:
        #     print("Inserting {}".format(task))
        #     insert_task(conn, task)

"""Get tar.gz, extract, then save to docs folder."""
def get_via_ftp(destination, ftp_location):
    import subprocess

    subprocess.run(
        ["curl", "-o", destination, "ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/{}".format(
                                                ftp_location)]
        )

def write_to_index(citation, pmcid):
    path = "../softcite-pdf-files/docs/pdf-files/pmc_oa_files/"
    index_file = path + "index.md"
    template = "  1. [{pmcid}: {cite}]({pmcid}.pdf)\n"
    with open(index_file, "a") as index_file:
        # 1. [2000-09-CELL.pdf](pdf-files/2000-09-CELL.pdf)
        index_file.write(template.format(cite = citation, pmcid = pmcid))

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
    pubs_to_code = get_pubs_to_code()
    shuffle(pubs_to_code)

    # [10,23] ==> [10,10,23,23]
    doubled_list = [x for item in pubs_to_code for x in repeat(item, 11)]

    for order, task in enumerate(doubled_list):
        insert_task(conn, order, task)

def insert_task(conn, task):
    print("Inserting {}".format(task))
    insert_sql = """INSERT INTO assignments(pub_id)
                         VALUE (%(task)s)
                 """
    conn.execute(insert_sql, {"task": task})
    if conn.rowcount == 1:
        print("Inserted {}".format(task))
    else:
        print("Failed to insert")

import os
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def get_username_from_github():
    import subprocess
    import re

    remotes_string = subprocess.check_output(
            ["git", "remote", "-v"]
    ).decode("utf8")
    # print(remotes_string)
    matches = re.search('origin.*github.com/(.*?)/softcite-dataset.git',
                        remotes_string)
    username = matches.group(1)
    if (username == "howisonlab"):
        username = "jameshowison"

    return username

def get_xml_for_pdf():
    path = "../softcite-pdf-files/docs/pdf-files/pmc_oa_files/"

    for filename in glob.iglob(path + "*.pdf"):
        matches = re.search("PMC(.*).pdf", filename)
        pmc_id = matches.group(1)
        tgz_destination = "{}/{}.tgz".format(path, pmc_id)
        xml_destination = "{}/PMC{}.xml".format(path, pmc_id)
        if not os.path.exists(xml_destination):
            download_xml_for_pmc_id(pmc_id, tgz_destination)
            extract_and_move_xml(path, pmc_id)

def download_xml_for_pmc_id(pmc_id, destination):
    import requests
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id="
    response_xml = requests.get(base_url + pmc_id).text
    print(response_xml)
    matches = re.search('format="tgz".*?href="(.*?)"', response_xml)
    tgz_url = matches.group(1)

    import subprocess

    subprocess.run(
        ["curl", "-o", destination, tgz_url]
        )

def extract_and_move_xml(path, pmc_id):
    import tarfile
    import re
    import shutil, os

    reT = re.compile(r'.*.nxml')

    tar_filename = "{}/{}.tgz".format(path, pmc_id)
    try:
        t = tarfile.open(tar_filename, 'r')
    except IOError as e:
        print(e)
    else:
        to_get = [m for m in t.getmembers() if reT.search(m.name)]
        t.extractall(path, members=to_get)
        print("Getting: {}".format(to_get))

    rename_xml_file(path, pmc_id)

def rename_xml_file(path, pmc_id):
    import shutil
    # get nxml filename
    path_s = "{}PMC{}/*.nxml".format(path, pmc_id)
    print(path_s)
    nxml_files = glob.glob(path_s)
    if(len(nxml_files) != 1):
        print("Found more than one nxml file")
        pprint.pprint(nxml_files)
        exit()
    else:
        print("Found file:")
        pprint.pprint(nxml_files[0])
        shutil.copy(nxml_files[0], path + "PMC" + pmc_id + ".xml")
        shutil.rmtree(path + "PMC" + pmc_id)

def export_assignment_csv(cursor):

    sql_query = """
        SELECT *
        FROM assignments
    """
    cursor.execute(sql_query)
    headers = ["id","pub_id","assigned","assigned_to","asssigned_timestamp"]
    with open('data/softcite_assignments.csv', 'w') as csvfile:
        myCsvWriter = csv.DictWriter(csvfile,
                    fieldnames = headers)
        myCsvWriter.writeheader()
        for row in cursor:
            # rather than 'for row in results'
            myCsvWriter.writerow(row)

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
    insert_pmc_tasks(cursor, int(sys.argv[1]))
    # export_assignment_csv(cursor)
    get_xml_for_pdf()
    # rename_xml_file("docs/pdf-files/pmc_oa_files/", "PMC5421183")
    # extract_and_move_xml("docs/pdf-files/pmc_oa_files/", "5421183")
    # This will fail unless on linux, should be run on
    # howisonlab anyway.

    # Check that script is run from right location.
    # neededPath = "code/getNextContentAnalysisAssignment.py"
    # if (sys.argv[0] != neededPath):
    #     raise Exception("Must run script from ~/softcite")
    #
    # username = sys.argv[1]
    # # print(username)
    # # username = pwd.getpwuid(os.getuid()).pw_name
    # # username = "tester"
    # pub_id = get_new_task(cursor, username)
    # generate_template_file(pub_id, username)

    # export_assignment_csv(cursor)

# """SELECT *
# FROM softcite_assignments
# INTO OUTFILE 'softcite_assignments.csv'
# FIELDS TERMINATED BY ','
# ENCLOSED BY '"'
# LINES TERMINATED BY '\n'"""
