import json
import os

import appdirs

path_to_data_dir = appdirs.user_data_dir("file-mover", "Ephraim Siegfried")
CONFIGS_DIR = os.path.join(path_to_data_dir, "configurations")
default_config = {
    "COMMAND": [
        {"FILE_EXTENSION(*)": "FILE_EXTENSION(*)"}],
    "WHERE_FROM": {},
    "NAME": {},
    "FILE_EXTENSION": {
        ".pdf": "./PDF",
        ".ps": "./PDF",
        ".jpg": "./Photos",
        ".jpeg": "./Photos",
        ".Jpeg": "./Photos",
        ".gif": "./Photos",
        ".HEIC": "./Photos",
        ".heic": "./Photos",
        ".JPG": "./Photos",
        ".jp2": "./Photos",
        ".png": "./Photos",
        ".svg": "./Photos",
        ".mov": "./Videos",
        ".MOV": "./Videos",
        ".mp4": "./Videos",
        ".docx": "./Word",
        ".odt": "./Word",
        ".doc": "./Word",
        ".pages": "./Word",
        ".pptx": "./PowerPoint",
        ".m4a": "./Audio",
        ".wave": "./Audio",
        ".wav": "./Audio"
    }
}
if not os.path.exists(path_to_data_dir):
    os.mkdir(path_to_data_dir)
    os.mkdir(CONFIGS_DIR)
    with open(os.path.join(CONFIGS_DIR, "default.json"), 'w') as f:
        json.dump(default_config, f, indent=2)


def get_config_path(name):
    return os.path.join(CONFIGS_DIR, name + ".json")


def get_list_of_configurations():
    return os.listdir(CONFIGS_DIR)


def print_list_configurations():
    configs = [c.replace('.json', '') for c in get_list_of_configurations()]
    print(*configs, sep="\n")


def open_configuration(name):
    os.system(f"open -e \"{get_config_path(name)}\"")  # TODO: Doesn't work for other OS than MACOS


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
