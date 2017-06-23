---
title: "Setting up Keyboard Shortcuts"
---
# Setting up Keyboard Shortcuts

Keyboard shortcuts are useful to speed up your work and prevent typos. Below are instructions on how to do initial shortcut set up as well as make changes to your settings later.

## Snippets

We use snippets to paste in most of the content of a data file. To set up your snippets you will run a script and edit your snippets.cson file.

### Setting up Snippets for the First Time

Your snippets file requires a certain format so that Atom can understand what shortcuts are able to be used with different languages. The indentation in your snippets file is meaningful. Because the Howison Lab uses snippets for both the Transition project and the Softcite project, but Atom only has one snippets file, you must follow the instructions in the order below, or the formatting will not be correct.

1. In the terminal, after signing into the lab server, switch directories to Transition

`$ cd transition/`

1. Run the following command. This command will execute a script that will write the text you will need to a file named mySnippet.

`$ python3 code/generateSnippet.py <your Github username> > mySnippet`

For example, if your Github username is jdoe, your command would look like:

`python3 code/generateSnippet.py jdoe > mySnippet`

1. In Atom, right click the transition directory and select "Refresh." A file named mySnippet should then appear.

1. Open the mySnippet file and select and copy the entire contents to your clipboard.

1. If you are using a Mac, click on the Atom menu and select "Snippets." If you are using a PC, click on File and select "Snippets." A file should open in Atom called snippets.cson.

1. Paste what you copied in step 4 below all of the comments in snippets.cson. Select everything you pasted and hit shift+tab until the first line *and only the first line* is as far left as it can go. It is important that you do not change the way the lines nest within one another; you want to move the entire block of content that you pasted leftward. The indentation and content should begin like this:

```'.source.turtle':
      'true':
        'prefix': 'tr'
        'body': 'true'
      'false':
        'prefix': 'fa'
        'body': 'false'
```

1. Save snippets.cson. Do not close the file.

1. Close the mySnippet file. Right click on the file in the file tree on the left and delete it.

1. In the terminal, switch directories to softcite-dataset. Assuming you are still in transition, you will execute this command:

`$ cd ../softcite-dataset/`

If you are not in transition still, you do not need the ../ in the above command.

1. Run the generateSnippet script again:

`$ python3 code/generateSnippet.py <your Github username> > mySnippet`

1. In Atom, right click the softcite-dataset directory and select "Refresh." The mySnippet file should appear.

1. Open the mySnippet file and select and copy the entire contents to your clipboard.

1. Paste the contents of the softcite-dataset mySnippet file into snippets.cson below the content you pasted earlier. This additional content should begin like this:

```'memo':
      'prefix': 'mem'
      'body': 'ca:memo ; # use triple  quotes'
```
1. Adjust the indentation of the content you just pasted in using shift+tab so that `'memo'` is one indentation in (i.e. it is parallel with 'true' in the example above). This new content must be nested within `'.source.turtle'` but not indented within any of the snippets you added already.

1. Save snippets.cson and close the file.

1. Delete and close mySnippet.

### Updating Snippets

If there is a new code added to the coding scheme or there has been a formatting change, you may need to update your snippets.cson file. To update your snippets follow these instructions.

2. In the terminal, change directory to the project whose snippets you will be updating. If you are updating softcite snippets, you would use this command:

`$ cd softcite-dataset/`

2. Run the generateSnippet script:

`$ python3 code/generateSnippet.py <your Github username> > mySnippet`

For example, if your Github username is jdoe, your command would look like:

`python3 code/generateSnippet.py jdoe > mySnippet`

2. In Atom, right click the directory for the project whose snippets you are updating and select "Refresh." A file named mySnippet should then appear.

2. Open the mySnippet file and select and copy the entire contents to your clipboard.

2. If you are using a Mac, click on the Atom menu and select "Snippets." If you are using a PC, click on File and select "Snippets." A file should open in Atom called snippets.cson.

2. Highlight all of the content that is associated with the project's snippets you are updating. If you are updating snippets for the Transition project, highlight all of the content from `'.source.turtle':` up until  `'memo':`; if you are updating snippets for Softcite, then highlight all of the content from `'memo':` until the end of the document. Delete the highlighted content.

2. Paste the content you copied in step 4 so that it replaces the content you just deleted.

2. Using shift+tab, adjust the indentation of the block of content you just pasted. See steps 6 and 13 of "Setting up Snippets for the First Time" for examples of what your indentation should look like.

2. Save snippets.cson and close the file.

2. Delete and close mySnippet.

## Keybinding

Follow these instructions to enable the time/date keybinding:

3. Ensure that you have installed the Date package in Atom. You can double check this by visiting preferences/settings (on a Mac vs. PC, respectively) and clicking on "Packages." If it is not installed, visit "Install" and search for "Date" then press "Install."

3. In your settings/preferences, click on "Packages" and then click on the "settings" button in the box for the Date package.

3. Update the Time Format field so that it reads: HH24:MI:SS

3. Update the Date Time Format field so that it reads: YYYY-MM-DDTHH24:MI:SS-05:00

3. Close your settings.

3. Find and open your keymap file. On a Mac, you will find this under the "Atom" menu. On a PC this will be listed under "File."

3. Paste the following content into the keymap.cson file, ensuring that the second line is indented within the first:

```'atom-text-editor':
      'shift-cmd-t': 'date:datetime'
```

3. Save and close keypmap.cson.
