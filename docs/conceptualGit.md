---
title: "Understanding Git"
---
[Return Home](index.md)

## A Maritime Business Lesson on Commits, Pushing, and Pulling
As you work, you will be making changes to your clone. You will want to save those changes. You will want to back up those changes to your fork on Github. You will also want to share those changes with the Howison Lab repo.

Imagine your folder on the lab server is an island. You are shipping goods to the mainland. In this metaphor, your changes to data files are those goods. As you change a file you will save it, like you would any file. Think of saving a file as boxing up a good—your recipient doesn't have it yet but it's a necessary first step in the process.

To prepare a shipment, you stack your boxed goods in rooms on a ship. Each box you carry from the warehouse to the ship is staging work for the eventual shipment. To be certain you're carrying everything you need, you scan the area to identify all the boxed up goods. A saved file can be staged in much the same way. In git, we do that scan using the `status` command—it will show us all the modified files we have. We use the `add` command to stage something.

You might be boxing and staging certain kinds of goods in chunks. For instance, you might box and stage your island produce in one room on the ship before moving on to your dry goods. When you've finished staging the produce, you shut the door on that room and record that you've finished with that chunk of work. Similarly, we will work on one thing at a time—a coded article. After we've staged our file by using the `add` command, we use the `commit` command to say, "Yes, I'm done with this bit of work." You can include a message with your commit to describe the piece of work, like recording that you finished staging the produce. With each article you code, you can `add` and `commit` it when you are finished working on it.

But, even after you've finished packing everything into the ship—you've committed to everything—the boat is still there on the island. No one else even knows that you finished packing. The boat needs to push off shore and head toward the dock at the main land. You can send off your committed work with the command `push`.

Your boat lands at a dock you own named `Origin` and your people can unload it. This is akin to your commits being available in your fork on Github.

All of that is great, and some people would stop there and call it a day. But you want your goods to be distributed to other people, so you need to have a store start stocking your goods. Everyone knows to go to a particular store to buy things, so you will ask that store to stock your products. If your dock is akin to your fork, the store is the Howison Lab repo. The Howison Lab repo is where the other students can get (buy) your data files (products).

So, you pack up your ship with your goods and leave the dock, moving `upstream` to the store. You can't just start putting things on the shelf yourself though, so you have to ask permission. With git, we would make a `pull` request of the Howison Lab, asking it to please incorporate our files into its repo.

The store inspects your goods, thinks they're great and puts them on the shelves. Now other people can take them home to their own islands, just as other students can see your files once they have been `merged` into the Howison Lab repo.

Sometimes the store comes out with a new product you have to have. In our case, that might be an update to the coding scheme. You order that product from the store and it shows up on your island along with all of the other new products from other island merchants. In git terms, to get those updates, we would `pull` the files from `upstream`—that would give us anything from the Howison Lab that we didn't already have—the new coding scheme and other students' data files.

None of this works properly if you do it out of order or skip a step. You can't commit to work if you haven't already staged it. Pushing to Origin won't do anything worthwhile if you haven't committed to any work. If you don't make a pull request, then Howison Lab will never have your changes. And, if there aren't any updated files in the Howison Lab repo, your pull upstream command will just come up empty.

[Return Home](index.md)
