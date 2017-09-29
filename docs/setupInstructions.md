---
title: "Working on Softcite Data Files"
---
[Return Home](index.md)

# Working on Softcite Data Files

This is the basic information you need to get into the Howison lab server and to commit your changes.

## Accessing the Lab Server

This is how you can access the lab's server where your work is stored:

### Macs

*If you are using a Mac:* Use Spotlight Search to search for "terminal." In the window that opens, enter the following command:

    `$ssh <lab username>@howisonlab.ischool.utexas.edu`

    *Note:* When shown a command to enter into the terminal (also referred to as the command line), the command will be prefaced with the dollar sign symbol: $. This is not a key that you are meant to type yourself, instead it means, "Type everything after this." For example, your login should look like this:

    ![Login Example](/images/loginExample.png)

    Enter your password after the prompt. As you type, it will not show you the characters.

### Windows (using Putty)

*If you are using a PC:* Open PuTTY. In the "User" field, enter your lab username. In the "Hostname" field, enter "howisonlab.ischool.utexas.edu" (do not use quotes yourself).

    Enter your password in the terminal window that opens.

### Access From Off Campus

When you need to connect to the server from home, you'll need to use a VPN. There is a university [wiki page](https://wikis.utexas.edu/pages/viewpage.action?spaceKey=networking&title=Connecting+to+the+UT+VPN+Service) that includes instructions on how to do this.  You will need to download CISCO AnyConnect, regardless of what kind of computer you use. You will also need to set up two factor authentication. The wiki page explains what you need.

When you are actually attempting to use AnyConnect, note that when you put your "Duo Passcode" in (in the empty field in the image below) you won't be typing your password for a second time, but entering "push," "SMS," or "phone" according to the instructions below that field.

![AnyConnect image](/images/anyconnect.png)

## Moving to the Right Repo

Once you've logged onto the server, you'll need to move to the correct folder. For now, we're only working on softcite work, so you'll change directories in the terminal:

  `$ cd softcite-dataset/`

## Opening the Server in Atom

To edit your server files, you'll need to open the folder that you made your .ftpconfig file in Atom. Then, you can open the FTP remote pane by going to packages>ftp remote>toggle. Then, from the pane that opens, you can hit connect. You can collapse the pane that has your .ftpconfig file in it—you won't need that.

## Checking for Errors

Before committing, you will need to confirm that there are no problems with your files. You will run the command pytest, and repair any errors if necessary.

1. Check if there are any errors:

    `$ pytest`

    If a file has an error, it will be shown under “FAILURES” and look like:

    `Failed: BadSyntax: Use python3 code/parseTurtle.py -f data/individuals--<username>/<filename>.ttl`

1. To find out exactly where the error in that particular file is, copy the line line that begins with `python3 code/`… and run that as a command:

    `$ python3 code/parseTurtle.py -f data/individuals-<username>/<filename>.ttl`

    The command will run and spew out something that ends with an error saying something like:

    `rdflib.plugins.parsers.notation3.BadSyntax: at line 330 of <>:`

1. In Atom, *if this was a file you edited*, visit the line number in the file (which was named after running the previous command) and resolve the error, save, commit, and push as described below.

## Committing Changes

When you need to save your changes, you will make a commit. The first step is to check what files have been changed. Then, add the files that are in your individuals folder (don't add anything in the cache or anything you don't remember modifying). Then double check you've added everything you need. Then make a commit and include a message. Finally, you'll push your changes up to your Github repo. Step by step:

2. View which files were modified:

    `$ git status`

2. Add the files you want:

    `$ git add <name of modified file>`

2. View which files were modified to check you got everything:

    `$ git status`

2. Enter your commit message:

    `$ git commit –m “<message content>”`

2. Push commit up to Github:

    `$ git push origin master`

2. After you have completely finished coding an article, you can make a pull request. To do that, visit your repo on Github and click the "New Pull Request" button.

## Requesting a New Article

When you have finished coding one article and committed your work, you can request another article to work on.

From the terminal, execute the following command followed by your github username:

  `$ python3 code/getNextContentAnalysisAssignment.py <username>`

A new file will be added to your individuals folder. You may need to right click on it and hit refresh to make the new file appear. The new file will contain the prefixes and article block for your new assignment.

[Return Home](index.md)
