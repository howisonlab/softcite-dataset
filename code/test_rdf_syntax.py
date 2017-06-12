import parseTurtle
import pytest
import rdflib

"""Defines a test that takes file_to_check as an argument"""
def test_individual_file_parse(file_to_check):
        g = rdflib.Graph()
        print("Parsing {}".format(file_to_check))
        print("Seek line numbers for errors with:")
        print("python3 code/parseTurtle.py -f {}".format(file_to_check))
        print("Use ctrl-G to jump to line number")
        g.parse(file_to_check, format="n3")

"""Uses metafunc to create a list of arguments for test_individual_file_parse"""
def pytest_generate_tests(metafunc):
    files = parseTurtle.find_all_turtle_files("data")
    metafunc.parametrize("file_to_check",files)

# @pytest.mark.parametrize("file_to_check", [
#         ("data/coding-scheme.ttl"),
#         ("data/individuals-Chriscuit/1047963.ttl")
#     ])
# def test_parse(file_to_check):
#     assert test_individual_file_parse(file_to_check)
