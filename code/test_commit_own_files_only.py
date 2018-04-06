from getUsername import get_username_from_github
import subprocess
import os


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
    ).decode("utf8")

    if username != "jameshowison":
        for file_name in files_changed:
            assert username in file_name, "File outside of individuals folder included in commit"
