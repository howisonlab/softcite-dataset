from parseTurtle import check_selections_in_body
from getUsername import get_username_from_github
import parseTurtle
import pytest
import rdflib

"""Defines a test that takes file_to_check as an argument"""

def test_individual_file_parse(file_to_check):
        g = rdflib.Graph()

        try:
            g.parse(file_to_check, format="n3")
            check_selections_in_body(g)
        except:
            pytest.fail("BadSyntax: Use python3 code/parseTurtle.py -f {}".format(file_to_check))

        assert len(g) > 0, "File should not be empty"

"""Uses metafunc to create a list of arguments for test_individual_file_parse"""
def pytest_generate_tests(metafunc):
    #get coder's username to reduce number of files parsed
    username = get_username_from_github()
    files = parseTurtle.find_all_turtle_files("data/individuals-{}/".format(username))
    assert len(files) > 0, "Must be files to check"
    #files = parseTurtle.find_all_turtle_files("data/")
    metafunc.parametrize("file_to_check", files)
