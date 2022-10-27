import json
import os


class MoveConfig:

    def __init__(self):
        # reads the config.json file
        json_config = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json"), "r")
        self.dic_config = json.load(json_config)
        self.command = self.dic_config["COMMAND"]
        self.where_from = self.dic_config["WHERE_FROM"]
        self.name = self.dic_config["NAME"]
        self.file_extension = self.dic_config["FILE_EXTENSION"]

    def get_command(self):
        return self.command

    def get_properties(self):
        return {key: value for key, value in self.dic_config.items() if key != "COMMAND"}
