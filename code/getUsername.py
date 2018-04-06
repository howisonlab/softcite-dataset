def get_username_from_github():
    import subprocess
    import re

    remotes_string = subprocess.check_output(
            ["git", "remote", "-v"]
    ).decode("utf8")
    # print(remotes_string)
    # remotes_list = remotes_string.split()
    # remote = remotes_list[1]
    # print(remote)
    matches = re.search('origin.*?github.com.(.*?)/softcite-dataset', remotes_string)
    username = matches.group(1)
    if (username == "howisonlab"):
        username = "jameshowison"

    return username.lower()
