'''
Simply apply the stopwords/blacklist to clean an existing json file from spurious entities.
Note that this cleaning is already done by applying the enrichJSON.py script, so this program 
should normally not be necessary.
'''
import os
import argparse
import ntpath
import json
from collections import OrderedDict
import pysbd
import re
from corpus2JSON import convert_to_sentence_segments
import requests

class Cleaner(object):    

    def __init__(self, config_path='./config.json'):
        # load config and white term list
        self.config = self._load_config(config_path)

        self.blacklist = []
        black_list_files = self.config["blacklist"]
        for file_string in black_list_files:
            print(os.path.join("../../data/software_lists/stop", file_string))
            with open(os.path.join("../../data/software_lists/stop", file_string)) as file:
                line = file.readline()
                while line:
                    if len(line.strip()) == 0:
                        continue
                    if line.strip() not in self.blacklist:
                        self.blacklist.append(line.strip())
                    line = file.readline()
        print("total", str(len(self.blacklist)), "stop terms")

    def _load_config(self, path='./config.json'):
        """
        Load the json configuration 
        """
        config_json = open(path).read()
        return json.loads(config_json)

    def clean(self, json_path, output_path):
        for file in os.listdir(json_path):
            if file.endswith(".json"):
                print(os.path.join(json_path, file))
                with open(os.path.join(json_path, file)) as jsonfile:
                    json_doc = json.load(jsonfile, object_pairs_hook=OrderedDict)
                    if "body_text" in json_doc:
                        for paragraph in json_doc["body_text"]:
                            entities = None
                            references = None
                            if "entity_spans" in paragraph:
                                entities = paragraph["entity_spans"] 
                                new_entities = []

                                for entity in entities:
                                    if entity['type'] != 'software':
                                        new_entities.append(entity)
                                    if entity['type'] == 'software' and not self.is_forbiden(entity['rawForm']):
                                        new_entities.append(entity)
                                    elif entity['type'] == 'software':
                                        # we need to remove the annotations corresponding 
                                        # to attribute of the software
                                        the_id = entity['id']
                                    

                                
                                if len(new_entities)>0:
                                    paragraph["entity_spans"] = new_entities
                                else:
                                    paragraph.pop("entity_spans")

                    output_file = os.path.join(output_path, file)
                    with open(output_file, 'w') as outfile:
                        json.dump(json_doc, outfile, indent=4)


    def is_forbiden(self, term):
        if term in self.blacklist:
            return True
        if term.isnumeric():
            return True
        if term.startswith("JHEP"):
            return True
        else: 
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Cleaning of software mention annotations present in lossy JSON format")
    parser.add_argument("--json-repo", type=str, 
        help="path to the directory of JSON files converted from TEI XML produced by GROBID, where the automatic annotations have been injected")
    parser.add_argument("--output", type=str, 
        help="path to an output directory where to write the cleaned JSON file(s)")
    parser.add_argument("--config", default="./config.json", help="path to the config file, default is ./config.json") 

    args = parser.parse_args()
    json_repo = args.json_repo
    output_path = args.output
    config = args.config

    # check path and call methods
    if json_repo is None or not os.path.isdir(json_repo):
        print("error: the path to the JSON files is not valid: ", json_repo)
        exit(0)

    cleaner = Cleaner(config)
    cleaner.clean(json_repo, output_path)

