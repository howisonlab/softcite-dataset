---
title: "Second Day Setup"
---
[Return Home](index.md)

# During the Second Meeting
Now that you have all the accounts that you will need going forward, you can move on with your setup. In this phase, you will be getting access to the Softcite repository where you will save the data you collect. You will also set up some keyboard shortcuts to make that collection easier.

## But, first, Sign in

Each time you work on the Softcite project you will need to access your folder on the lab server. This means you will need to sign in (like you did last time to create your .ftpconfig file). To sign in:

*If you are using a Mac:* Use Spotlight Search to search for "terminal." In the window that opens, enter the following command:

    `$ssh <lab username>@howisonlab.ischool.utexas.edu`

    *Note:* When shown a command to enter into the terminal (also referred to as the command line), the command will be prefaced with the dollar sign symbol: $. This is not a key that you are meant to type yourself, instead it means, "Type everything after this." For example, your login should look like this:

    ![Login Example](/images/loginExample.png)


*If you are using a PC:* Open PuTTY. In the "User" field, enter your lab username. In the "Hostname" field, enter "howisonlab.ischool.utexas.edu" (do not use quotes yourself).

    Enter your password in the terminal window that opens.

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

1. In your terminal window, from your home directory (see the [example image above](homeDirectoryExample)), type the following command:

    `$git clone <copied HTTPS URL>`

Remember, you do not type the $ yourself. Do not put the angled brackets in your command. See this example:

    ![Git Clone Command](/images/gitClone.png)

1. In Atom, right click on your home directory. Then click **Refresh**. You should see a folder called softcite-dataset appear.

    ![Refresh](/images/refresh.png)

You have now created your own fork of the  Softcite repo and cloned it to your folder on the lab server!

## Set up Your Remotes

## Set up Your Keyboard Shortcuts

## Open the Coding Scheme

[Return Home](index.md)
