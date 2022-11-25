import json
import os
import subprocess
import sys

import appdirs
import logging

logger = logging.getLogger(__name__)

path_to_data_dir = appdirs.user_data_dir("fmover")
CONFIGS_DIR = os.path.join(path_to_data_dir, "configurations")


def get_config_path(name):
    """
    :param name: The name of the configuration without the .json extension
    :return: The absolute path to the configuration file
    """
    return os.path.join(CONFIGS_DIR, name + ".json")


def get_list_of_configurations():
    return os.listdir(CONFIGS_DIR)


def print_list_configurations():
    configs = [c.replace('.json', '') for c in get_list_of_configurations()]
    print(*configs, sep="\n")


def open_configuration(name):
    file_path = get_config_path(name)
    if sys.platform == 'win32':
        subprocess.Popen(['start', file_path], shell=True)
    elif sys.platform == 'darwin':
        subprocess.Popen(['open', file_path])
    else:
        try:
            subprocess.Popen(['xdg-open', file_path])
        except OSError:
            logger.error("Could not open file in text editor")


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


def get_default_config():
    return {"COMMAND": [{"FILE_EXTENSION(*)": "FILE_EXTENSION(*)"}], "WHERE_FROM": {}, "NAME": {}, "FILE_EXTENSION": {
        ".pdf": "./PDF", ".ps": "./PDF", ".jpg": "./Photos", ".jpeg": "./Photos", ".Jpeg": "./Photos",
        ".gif": "./Photos",
        ".HEIC": "./Photos", ".heic": "./Photos", ".JPG": "./Photos", ".jp2": "./Photos", ".png": "./Photos",
        ".svg": "./Photos", ".mov": "./Videos", ".MOV": "./Videos", ".mp4": "./Videos", ".MP4": "./Videos",
        ".m4v": "./Videos", ".M4V": "./Videos", ".avi": "./Videos", ".AVI": "./Videos", ".docx": "./Text",
        ".odt": "./Text", ".doc": "./Text", ".pages": "./Text", ".txt": "./Text", ".rtf": "./Text",
        ".pptx": "./PowerPoint", ".m4a": "./Audio", ".wave": "./Audio", ".wav": "./Audio"}}


def initialize_configuration_directory():
    if not os.path.exists(path_to_data_dir):
        os.mkdir(path_to_data_dir)
        os.mkdir(CONFIGS_DIR)
        with open(os.path.join(CONFIGS_DIR, "default.json"), 'w') as f:
            json.dump(get_default_config(), f, indent=2)
