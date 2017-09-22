---
title: "Updating Snippets"
---
[Return Home](index.md)

# Updating Snippets

If there is a new code added to the coding scheme or there has been a formatting change, you may need to update your snippets.cson file. To update your snippets follow these instructions.

2. In the terminal, change directory to the project whose snippets you will be updating. If you are updating softcite snippets, you would use this command:

    `$ cd softcite-dataset/`

2. Commit any changes you have. See Committing Changes in the [Working on Softcite Data Files](setupInstructions#committing-changes) page for a refresher on how to do this.

2. Pull the latest changes from the Howison Lab repo:

    `$ git pull upstream master`

2. Run the generateSnippet script:

    `$ python3 code/generateSnippet.py <your Github username> > mySnippet`

    For example, if your Github username is jdoe, your command would look like:

    `python3 code/generateSnippet.py jdoe > mySnippet`

2. In Atom, right click the directory for the project whose snippets you are updating and select "Refresh." A file named mySnippet should then appear.

2. Open the mySnippet file and select and copy the entire contents to your clipboard.

2. If you are using a Mac, click on the Atom menu and select "Snippets." If you are using a PC, click on File and select "Snippets." A file should open in Atom called snippets.cson.

2. Highlight all of the content that is associated with the project's snippets you are updating. If you are updating snippets for the Transition project, highlight all of the content from `'.source.turtle':` up until  `'memo':`; if you are updating snippets for Softcite, then highlight all of the content from `'memo':` until the end of the document. Delete the highlighted content.

2. Paste the content you copied earlier so that it replaces the content you just deleted.

2. Using shift+tab, adjust the indentation of the block of content you just pasted. See steps 6 and 13 of [Setting up Snippets for the First Time](#setting-up-snippets-for-the-first-time) for examples of what your indentation should look like.

2. Save snippets.cson and close the file.

2. Delete and close mySnippet.


[Return Home](index.md)
