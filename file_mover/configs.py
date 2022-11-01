import json
import os

CONFIGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")


def config_path(name):
    return os.path.join(CONFIGS_DIR, name + ".json")


def list_configurations():
    configs = os.listdir("/Users/ephraimsiegfried/PycharmProjects/DownloadsMover/configs")
    print(*configs, sep= "\n")


def open_configuration(name):
    os.system("open -e "+ config_path(name)) # TODO: Doesn't work for other OS than MACOS


def print_configuration(name):
    config = open(config_path(name))
    print(json.dumps(json.load(config), indent= 2))


def create_configuration(name):
    template = {"COMMAND": [{}], "WHERE_FROM": {}, "NAME": {}, "FILE_EXTENSION": {}}
    json_object = json.dumps(template, indent=2)
    with open(f"{os.path.join(CONFIGS_DIR, name)}.json", "w") as outfile:
        outfile.write(json_object)
