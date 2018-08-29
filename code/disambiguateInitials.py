# disambiguates coders initials.
import glob


map_change = {"carsonbrown19": {"current": "_CB",
                                "desired": "_CBrown"}}

dir_to_check = "data"

# files += glob.glob(dir_to_check + "*.ttl")
# Add individuals for those to be changed
for coder, exchange in map_change.items():
    files = []
    files.extend(
        glob.glob(dir_to_check +
                  "/individuals-{}/*.ttl".format(coder))
    )

    for filename in files:
        # from https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file-using-python/20593644#20593644
         # Read in the file
        with open(filename, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(exchange["current"],
                                    exchange["desired"])

        # Write the file out again
        with open(filename, 'w') as file:
            file.write(filedata)

# PMC3281721_TZ07
