import json
import os

CONFIGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configurations")


def get_config_path(name):
    return os.path.join(CONFIGS_DIR, name + ".json")


def get_list_of_configurations():
    return os.listdir(CONFIGS_DIR)


def print_list_configurations():
    configs = get_list_of_configurations()
    print(*configs, sep="\n")


def open_configuration(name):
    os.system("open -e " + get_config_path(name))  # TODO: Doesn't work for other OS than MACOS


def print_configuration(name):
    config = open(get_config_path(name))
    print(json.dumps(json.load(config), indent=2))


def create_configuration(name):
    template = {"COMMAND": [{}], "WHERE_FROM": {}, "NAME": {}, "FILE_EXTENSION": {}}
    json_object = json.dumps(template, indent=2)
    with open(f"{os.path.join(CONFIGS_DIR, name)}.json", "w") as outfile:
        outfile.write(json_object)


def delete_configuration(name):
    os.remove(get_config_path(name))
