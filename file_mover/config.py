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

    def __assert_parameters_are_correct(self):
        config_keys = self.dic_config.keys()
        return "WHERE_FROM" in config_keys and \
               "NAME" in config_keys and \
               "COMMAND" in config_keys and \
               "FILE_EXTENSION" in config_keys
