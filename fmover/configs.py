import json
import os
import subprocess
import sys


class MoveConfigsHandler:
    """
    This class is responsible for monitoring the configurations directory, updating the configurations and reporting
    about them.

    Attributes:
        CONFIGS_DIR: The absolute path to the configurations directory

    Methods:
        get_config_path(config_name): Returns the absolute path to the configuration file
        list_configs(): Returns a list of all the configuration files in the configurations directory
        print_configs(): Prints all the configurations in the configurations directory
        print_config_content(config_name): Prints the content of the configuration file
        open_config(config_name): Opens the configuration file in the default text editor
        delete_config(config_name): Deletes the configuration file
        create_config(config_name): Creates a new configuration file
        get_default(): Returns the default configuration
    """

    def __init__(self, path_to_data_dir):
        self.CONFIGS_DIR = os.path.join(path_to_data_dir, "configurations")
        if not os.path.exists(path_to_data_dir):
            os.mkdir(path_to_data_dir)
            os.mkdir(self.CONFIGS_DIR)
            with open(os.path.join(self.CONFIGS_DIR, "default.json"), 'w') as f:
                json.dump(self.get_default(), f, indent=2)

    def get_config_path(self, config_name) -> str:
        """
        :param config_name: The name of the configuration file without the extension
        :return: The absolute path to the configuration file
        """
        return os.path.join(self.CONFIGS_DIR, config_name + ".json")

    def list_configs(self) -> list:
        """
        :return: A list of all the configuration files in the configurations directory
        """
        return [f[:-5] for f in os.listdir(self.CONFIGS_DIR) if f.endswith(".json")]

    def print_configs(self) -> None:
        """
        Prints all the configurations in the configurations directory
        """
        configs = [c.replace('.json', '') for c in self.list_configs()]
        print(*configs, sep="\n")

    def print_config_content(self, config_name) -> None:
        """
        Prints the content of the configuration file
        :param config_name: The name of the configuration file without the extension
        """
        config_path = self.get_config_path(config_name)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The configuration file {config_name} does not exist. "
                                    f"Choose one from the following: {self.list_configs()}")
        with open(config_path, 'r') as f:
            print(f.read())

    def open_config(self, config_name) -> None:
        """
        Opens the configuration file in the default text editor
        :param config_name: The name of the configuration file without the extension
        """
        config_path = self.get_config_path(config_name)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The configuration file {config_name} does not exist. "
                                    f"Choose one from the following: {self.list_configs()}")
        if sys.platform == "win32":
            os.startfile(config_path)
        elif sys.platform == "darwin":
            subprocess.call(('open', config_path))
        else:
            subprocess.call(('xdg-open', config_path))



    def delete_config(self, config_name) -> None:
        """
        Deletes the configuration file
        :param config_name: The name of the configuration file without the extension
        """
        config_path = self.get_config_path(config_name)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"The configuration file {config_name} does not exist."
                                    f" Choose one from the following: {self.list_configs()}")
        os.remove(config_path)

    def create_config(self, config_name) -> None:
        """
        Creates a new configuration file
        :param config_name: The name of the configuration file without the extension
        """
        config_path = self.get_config_path(config_name)
        if os.path.exists(config_path):
            raise FileExistsError(f"The configuration file {config_name} already exists. "
                                  f"These are the existing configurations: {self.list_configs()}")
        with open(config_path, 'w') as f:
            json.dump(self.get_template(), f, indent=2)

    def get_default(self):
        return {"COMMAND": [{"FILE_EXTENSION(*)": "FILE_EXTENSION(*)"}], "WHERE_FROM": {}, "NAME": {},
                "FILE_EXTENSION": {
                    ".pdf": "./PDF", ".ps": "./PDF", ".jpg": "./Photos", ".jpeg": "./Photos", ".Jpeg": "./Photos",
                    ".gif": "./Photos",
                    ".HEIC": "./Photos", ".heic": "./Photos", ".JPG": "./Photos", ".jp2": "./Photos",
                    ".png": "./Photos",
                    ".svg": "./Photos", ".mov": "./Videos", ".MOV": "./Videos", ".mp4": "./Videos", ".MP4": "./Videos",
                    ".m4v": "./Videos", ".M4V": "./Videos", ".avi": "./Videos", ".AVI": "./Videos", ".docx": "./Text",
                    ".odt": "./Text", ".doc": "./Text", ".pages": "./Text", ".txt": "./Text", ".rtf": "./Text",
                    ".pptx": "./PowerPoint", ".m4a": "./Audio", ".wave": "./Audio", ".wav": "./Audio"}}

    def get_template(self):
        return {"COMMAND": [{}], "WHERE_FROM": {}, "NAME": {}, "FILE_EXTENSION": {}}

