import json
import os


class MoveConfig:

    def __init__(self, config_json_path):
        # reads the config.json file
        json_config = open(config_json_path, "r")
        self.dic_config = json.load(json_config)
        self.commands = self.dic_config["COMMAND"]

    def get_commands(self) -> list:
        return self.commands

    def get_properties(self) -> dict:
        return {key: value for key, value in self.dic_config.items() if key != "COMMAND"}


