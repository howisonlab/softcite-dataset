import parseTurtle
import pytest
import rdflib

"""Defines a test that takes file_to_check as an argument"""
def test_individual_file_parse(file_to_check):
        g = rdflib.Graph()

        try:
            g.parse(file_to_check, format="n3")
        except rdflib.plugins.parsers.notation3.BadSyntax as bs:
            pytest.fail("BadSyntax: Use python3 code/parseTurtle.py -f {}".format(file_to_check))

        assert len(g) > 0, "File should not be empty"

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
