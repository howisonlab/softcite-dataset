---
title: "How to Ask for Help"
---
[Return Home](index.md)

## How to Ask for Help

If you run into a problem while working on Softcite data collection, you can email Hannah for help at johannacohoon@gmail.com. First, you should try to resolve the issue on your own, however. To try to figure out your problem on your own, do a web search. Stack Overflow is a question and answer site with reliably helpful answers. If you got an error message in the terminal, it's likely that the internet knows something about it. Some other basic things to try before emailing are:

1. Try pulling upstream: `git pull upstream`. You will need to commit first.

1. If you're having problems committing, do a `git status` to see if your files have all been staged.

1. If your error check is failing because of a file that is not in your individuals folder, just ignore it.

1. Check where you are in your directory. Don't run commands directly from your individuals folder. Do it from softcite-dataset. This means that your terminal should show you as being in /home/userName/softcite-dataset when you run `pwd` (print working directory)—not in /home/userName/softcite-dataset/data/individuals-userName.

1. If working off campus, ensure you're using the VPN.

1. If Atom is giving you trouble, make sure your .ftpconfig file is open.

When emailing, to get the best help as quickly as possible, please follow these guidelines:

1. Describe the issue by including *specific* details of what you were working on and what you were trying to do. For example, instead of saying, "I got an error in the terminal and can't commit," you could say, "I added the files that I was working on but I left one file unstaged because it wasn't in my individuals folder. When I ran `git commit -m` I got the following error: xyz."

1. Include a screenshot. Take a screenshot of the entire window—don't crop it so that only the error is visible. It's useful to see what else is on the screen.

1. Tell me what you've done so far to try to figure out what's going on. If you've tried pulling upstream, tell me. If you've double checked that your .ftpconfig file is open, tell me.

[Return Home](index.md)
