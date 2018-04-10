import os
import subprocess
import re

def get_username_from_github():
    if "TRAVIS_PULL_REQUEST_SLUG" in os.environ:
        if os.environ["TRAVIS_PULL_REQUEST_SLUG"] != "":
            repo_string = os.environ["TRAVIS_PULL_REQUEST_SLUG"]
        else:
            repo_string = os.environ["TRAVIS_REPO_SLUG"]

        username, _ = repo_string.split("/")
    else:
        remotes_string = subprocess.check_output(
              ["git", "remote", "-v"]
        ).decode("utf8")
        matches = re.search('origin.*?github.com.(.*?)/softcite-dataset', remotes_string)
        username = matches.group(1)

    if (username == "howisonlab"):
        username = "jameshowison"

    return username.lower()
