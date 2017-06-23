---
title: "Viewing the Coding Scheme in HTML"
---
# Viewing the Coding Scheme in HTML

The coding scheme .ttl file is not always easy to read and a printed version will not always be up to date. To ensure that you have an up to date version and eliminate any difficulty in reading it, follow the instructions below.

When you have an up to date HTML coding scheme, all you need to do to use it is open the coding-scheme.html file under docs, right click over the open file, and click on "view in browser." Then, go to your open browser and find the table that Atom opened for you.

## Using the HTML Coding Scheme for the First Time

1. In the terminal, after signing into the lab server, switch directories to softcite-dataset:

    `$ cd softcite-dataset/`

1. Run the following command. This command will execute a script that will create the HTML file you need:

    `python3 code/generate_coding_scheme_html.py > docs/coding-scheme.html`

1. In Atom, under the softcite-dataset directory, expand the docs folder and double click to open coding-scheme.html.

1. Hovering over the open file (not the file name in the navigation tree), right click click on "view in browser." This will not work if you have not yet installed the browser-plus package. Visit your preferences to install that package if necessary.

1. Visit your web browser to see the HTML file. Atom will not automatically direct you to the new tab even though it opens the file for you, so you must click to the browser yourself. If it works, you should see a table version of the coding scheme with a blue background.

## Updating the HTML Coding Scheme

If the coding scheme has changed, you will need to update your coding-scheme.html file so that it reflects the most recent version. To update your HTML file, follow these instructions:

2. In the terminal, after signing into the lab server, switch directories to softcite-dataset:

    `$ cd softcite-dataset/`

2. Commit any changes you have. See Committing Changes in the [Working on Softcite Data Files](setupInstructions) page for a refresher on how to do this.

2. Pull the latest changes from the Howison Lab repo:

    `$ git pull upstream master`

2. Execute steps 2-5 from [Using the HTML Coding Scheme for the First Time](#Using the HTML Coding Scheme for the First Time) above. This will run a script that writes over the old HTML file with the new contents.
