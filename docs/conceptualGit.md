## A Lesson on Commits, Pushing, and Pulling
As you work, you will be making changes to your clone. You will want to save those changes. You will want to back up those changes to your fork on Github. You will also want to share those changes with the Howison Lab repo.

Imagine your folder on the lab server is an island. You are shipping goods to the mainland. In this metaphor, your changes to data files are those goods. As you change a file you will save it, like you would any file. Think of saving a file as boxing up a good—your recipient doesn't have it yet but it's a necessary first step in the process.

To prepare a shipment, you stack your boxed goods on a ship. Each box you carry from the warehouse to the ship is staging work for the eventual shipment. A saved file can be staged in much the same way. In git, we use the `add` command to put something in staging.

You might be boxing and staging certain kinds of goods in chunks. For instance, you might box and stage your island produce in one room on the ship before moving on to your dry goods. When you've finished staging the produce, you shut the door on that room and record that you've finished with that chunk of work. This isn't irreversible, but it'd be a giant pain in the but to unlock and unpack all that stuff. Similarly, we will work on one thing at a time—a coded article. After we've staged our file by using the `add` command, we use the `commit` command to say, "Yes, I'm done with this bit of work." You can include a message with your commit to describe the piece of work, like recording that you finished staging the produce. With each article you code, you can `add` and `commit` it when you are finished working on it.

But, even after you've finished packing everything into the ship—you've committed to everything—the boat is still there on the island. No one else even knows that you finished packing. The boat needs to push off shore and head toward the dock at the main land. We can send off our committed work with the command `push`.

Your boat lands at the dock and your people unload it. This is akin to your commits being available in your fork on Github.

You want your goods to be distributed to other people. To make that happen, you need to b
