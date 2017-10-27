---
title: "Second Day Setup"
---
[Return Home](index.md)

# During the Second Meeting
Now that you have all the accounts that you will need going forward, you can move on with your setup. In this phase, you will be getting access to the Softcite repository where you will save the data you collect. You will also set up some keyboard shortcuts to make that collection easier.

## But, first, sign in

Each time you work on the Softcite project you will need to access your folder on the lab server. This means you will need to sign in (like you did last time to create your .ftpconfig file). To sign in:

*If you are using a Mac:* Use Spotlight Search to search for "terminal." In the window that opens, enter the following command, then enter your username and password as prompted. Remember not to type the $ or angled brackets.

    `$ssh <lab username>@howisonlab.ischool.utexas.edu`

*If you are using a PC:* Open PuTTY. In the "Hostname" field, enter "howisonlab.ischool.utexas.edu" (do not use quotes yourself). Enter your username and password in the terminal window that opens.

You are now logged into the lab server and are in your home directory. Your home directory will house any files or folders (like the Softcite repository) that you place there. Other students in the lab each have their own home directory. You can confirm that you are in your home directory by looking in the terminal window at the text that precedes your cursor. It should say yourUserName@howisonlab, like in the example below.

[![Directory example](/images/homeDirectoryExample.png)](#homeDirectoryExample)

## Fork and Clone the Softcite Repo
You will put a copy of the Softcite repository (AKA repo) in your folder on the lab server. A repository is a place where you can store things, in this case we are storing data and code. The Howison Lab maintains another copy of the repository that will include all the data that you share with it (through an action called *pushing*). Sometimes there might be changes to code files or the coding scheme. Those changes will be put in the Howison Lab's copy of the repo where you can *pull* those changes as they are made.

To make this happen, you first need to *fork* the Howison Lab's repo so that you have your own copy on Github. Then you will *clone* (copy) the your copy of the repo to your own directory on the lab server. Follow these instructions to do so:

1. Make sure you are signed in to the lab server by following the instructions in the previous section, if you haven't already.

1. In Atom, open the folder you made last time, titled howisonLabOnServer. That folder should have your .ftpconfig file in it.

1. Toggle the Remote-FTP package (click **Packages** on the top navigation bar, then **Remote-FTP**, then **Toggle**) and click **Connect** in the pane that opens. You should then see your nearly empty directory on the lab server.

1. You can collapse the pane that has "howisonLabOnServer" on top by hovering over it and clicking the collapse button that appears. The howisonLabOnServer pane shows you files that you have locally on your computer. We don't want those—you will be working with the files on the lab server.

1. Open your browser and go to https://github.com/howisonlab/softcite-dataset.

1. In the top right of that page, there is a button that says "Fork." Click **Fork** and in the window that pops up, asking "Where should we fork this repository?" select your account.

1. You should have just been brought to a page that at the top left shows you yourUserName/softcite-dataset.

    ![Fork](/images/fork.png)

    You are now in your *fork* of the Softcite repo. That means that, on Github, you now have your own copy of the repo. As you make changes to those files, they will not affect the Howison Lab repo unless you make a specific request for them to. This fork is only available on Github, however. It is not yet *cloned* to your folder on the lab server. That is the next step

1. On the right side of the page there is a green button that reads, "Clone or download." Click the **Clone or download** button and make sure you have the HTTPS option selected. You might need to click **Use HTTPS** to be sure of that. Copy the URL in the Clone with HTTPS window.

    ![Clone](/images/clone.png)

1. In your terminal window, from your home directory (see the example image above in "But, first, sign in"), type the following command:

    `$git clone <copied HTTPS URL>`

    Remember, you do not type the $ yourself. Do not put the angled brackets in your command. See this example:

    ![Git Clone Command](/images/gitClone.png)

1. In Atom, right click on your home directory. Then click **Refresh**. You should see a folder called softcite-dataset appear.

    ![Refresh](/images/refresh.png)

You have now created your own fork of the  Softcite repo and cloned it to your folder on the lab server!

## Set up Your Remotes
When you forked from the Howison Lab repo and cloned your fork, git made connections between your repo on the lab server and your fork on Github. Thats great, but you need a way for your fork to communicate with the Howison Lab repo. *Remotes* will let you communicate between those three versions of the Softcite repo.

When you made your clone, git automatically made one remote for you. To see that remote, follow these instructions:

1. In your open terminal window, after having logged in, *change directories* so that you are in the softcite-dataset folder, rather than your home folder. To do that, type the following command and hit enter:

    `$cd softcite-dataset`

1. To ask git to show you the remote it's made already, in the terminal type the following command and hit enter:

    `$git remote -v`

    That should show you two rows of text in three columns. The first column is the name of the remote. Yours should be called origin. Origin is your fork on Github. You know that because the next column provides you with the remote's address, which should be the URL that points to your fork. The third column reads *fetch* or *push*. Fetching means that you are asking for updates. We won't do that much. Pushing means you are sending your changes. We will do that a lot.

You will need to create another remote yourself. Follow these instructions to do so:

1. In your browser, go to the Howison Lab Softcite repo: https://github.com/howisonlab/softcite-dataset

1. Click **Clone or download** and copy the HTTPS URL like you did before.

1. In the terminal, type the following command and hit enter. Do not use the angled brackets in your command:

    `$git remote add upstream <howisonlab HTTPS for softcite>`

    This command created a new remote named *upstream* (a standard name for remotes in git) that points to the Howison Lab's Softcite repo on Github.

1. Enter one more command into the terminal that should help you not need to enter your password too frequently. Copy and paste this into your terminal and hit enter:

    `$ git config --global credential.helper 'cache --timeout=3600'`

## Set up Your Snippets
We have set up a number of keyboard shortcuts that should make your work easier. These are called snippets. You will run a python script that will output a file containing the code you need to set up your snippets.

Your snippets file requires a certain format so that Atom can understand what shortcuts are able to be used with different languages. The indentation in your snippets file is meaningful. Ask for help if you need. Follow these instructions to set up your snippets:

1. In Atom, in the top navigation bar, click on **Atom** (**File**, if you're on a PC) and select **Snippets**.  A file should open in Atom called snippets.cson.

1. Paste the following code into that file, below all of the comments that are already there. Include the single quotation marks.

    ```
      '.source.turtle':
          'true':
            'prefix': 'tr'
            'body': 'true'
          'false':
            'prefix': 'fa'
            'body': 'false'
    ```

1. Select everything you just pasted and hit shift+tab until the first line *and only the first line* is as far left as it can go. It is important that you do not change the way the lines nest within one another; you want to move the entire block of content that you pasted leftward, not one line at a time. The indentation and content should look just like the code you copied from above.

1. In the terminal, double check that you are in the softcite-dataset directory. You can check by using the print working directory command:

    `$ pwd`

    If the file path it lists ends in /softcite-dataset, you are in the correct directory. Otherwise, if it ends in your username, switch directories to softcite-dataset:

    `$ cd softcite-dataset/`

1. Run the following command, substituting your own Github username for "jdoe." Keep the angled bracket. This command will execute a script that will output the text you need into a file named mySnippet.

    `$ python3 code/generateSnippet.py jdoe > mySnippet`

1. In Atom, right click the softcite-dataset directory and select "Refresh." A file named mySnippet should then appear.

1. Open the mySnippet file, select the entire contents of the file, and copy it to your clipboard. Paste it in snippets.cson on the next line below what you pasted in previously. This additional content should begin like this:

    ```
      'memo':
          'prefix': 'mem'
          'body': 'ca:memo ; # use triple  quotes'
    ```

    You want 'memo' to be indented to the same degree as 'false' above it. Select the entirety of the text you pasted during this step and use tab to move outward or shift+tab as necessary.

    Do not have any blank lines between the code blocks you pasted.

1. Save snippets.cson.

1. In mySnippet, delete all of the text. On the very bottom of your Atom window, you should see something that reads "Plain Text." Click it.

1. In the window that popped up, search for "Turtle" and select the Turtle option.

1. Test your snippets by typing "itb" in your now empty mySnippet file. Hit tab on your keyboard. A bunch of text should appear.

    If it doesn't, double check that you changed "Plain Text" to Turtle, check that you don't have empty lines between the code you pasted into snippets.cson, and check that your indentation matches the examples. Be sure to save snippets.cson after any changes and before testing. Ask for help if you still have trouble.

1. If your text appeared, you can close the mySnippet file. Right click on the file in the file tree and delete it.


[Return Home](index.md)
