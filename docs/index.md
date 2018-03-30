---
title: "PDFs for softcite"
---
# Instructions

[First Day Setup](firstDay.md)

[Second Day Setup](secondDay.md)

[Coding Scheme](coding-scheme.html)

[Working on Softcite Data Files](setupInstructions.md)

[Update Snippets](shortcuts.md)

[Understanding Git in our Context](conceptualGit.md)

[Git and Github resources](gitResources.md)

[Asking for Help](askForHelp.md)

# October re-fork

1. Make a backup copy of your repo on howisonlab.

```
$ mv softcite-dataset softcite-dataset.bak
```

2. Delete your fork on Github.

3. Re-fork, go to [howisonlab/softcite-dataset](github.com/howisonlab/softcite-dataset)

4. Clone your fork to howisonlab

5. Move files from your backup to your new clone.

```
diff -qr softcite-dataset.bak/data/individuals-jameshowison/ softcite-dataset/data/individuals-jameshowison/
```

6. Copy over files from .bak

```
$ cp softcite-dataset.bak/data/individuals-jameshowison/jameshowison-PMC....ttl softcite-dataset/data/individuals-jameshowison/
```

7. Check them into the clean softcite-dataset

```
$ git status
$ git add <each file>
$ git commit
$ git push
# --> go to your fork on github and make pull request
```

# Links to Practice Files

1. [2000-22-AM_J_BOT.pdf](https://github.com/howisonlab/softcite-pdf-files/blob/master/docs/pdf-files/2000-22-AM_J_BOT.pdf)
1. [2004-40-NAT_GENET.pdf](https://github.com/howisonlab/softcite-pdf-files/blob/master/docs/pdf-files/2004-40-NAT_GENET.pdf)
