from getUsername import get_username_from_github
import subprocess
import os
import pprint


"""Ensure only including files in the users folder.
"""


def test_no_changes_outside_individuals_folder():
    try:
        range = os.environ["TRAVIS_COMMIT_RANGE"]
    except Exception as e:
        range = "HEAD..origin/master"

    username = get_username_from_github()
    files_changed = subprocess.check_output(
            ["git", "diff", "--name-only", range]
    ).decode("utf8").strip().split("\n")

    pprint.pprint(files_changed)
    pprint.pprint(username)
    if username != "jameshowison":
        for myfile in files_changed:
            print("is {} in {}".format(username, myfile))
            assert username in myfile, "File outside of individuals folder included in commit"
