import sys
import traceback
import os

from filemover.config_reader import MoveConfig
from logger import logger


def get_type(mapping: str):
    if mapping.find("(") < 0:
        logger.debug("Syntax is wrong" + mapping)
        return
    return mapping[0:mapping.find("(")]


def get_key(mapping):
    if mapping.find("(") < 0 or mapping < ")" < 0:
        logger.debug("Syntax is wrong" + mapping)
        return
    return mapping[mapping.find("(") + 1:mapping.find(")")]


class Mover:

    def __init__(self, properties):
        self.properties = properties
        self.config = MoveConfig()
        self.command = self.config.get_command()

    def corresponds(self, token):
        key = get_key(token)
        typ = get_type(token)
        for dictionary in self.config:
            if list(dictionary)[0] == typ:
                if key == "*":  # search for correspondence in any property of this type
                    for entry in dictionary.keys():
                        if entry in self.properties[typ]:
                            return dictionary[entry]  # The path where it should go to
                else:
                    if key in self.properties[typ]:
                        return dictionary[key]  # The path where it should go to
                    else:
                        return None  # no correspondence has been found

    def is_correspondence(self, ante):
        return self.corresponds(ante) is not None

    def parse_command(self):
        options = self.command.split(",")
        for option in options:
            condition = option.split("->")
            antecedent = condition[0].strip()
            consequent = condition[1].strip()
            matches = True
            for token in antecedent.split("&"):
                matches = self.is_correspondence(token.strip())
            if matches:
                logger.info("Executed command : " + option)
                return self.corresponds(consequent)
        return None


def main():
    if len(sys.argv) < 2:
        logger.warning("Arguments are missing")
        exit(126)

    # If you want to add a new property add it in file_properties and in move_config.txt
    path_to_go: str = None
    if sys.argv[2] is None:
        sys.argv[2] = "%"

    try:
        file = sys.argv[1]
        name, suffix = os.path.splitext(file.split("/")[-1]) if "/" in file else os.path.splitext(file)
        file_properties = {"WHEREFROM": sys.argv[2], "NAME": name,
                           "SUFFIX": suffix}
        path_to_go = Mover(file_properties).parse_command()
    except Exception as e:
        logger.exception("Exception occured: " + traceback.format_exc())

    if path_to_go is None:
        logger.info("File not moved: " + file.split("/").pop())
        return file
    logger.info("File " + file.split("/").pop() + " moved to: " + path_to_go + "\n")
    print(path_to_go)
    return path_to_go


if __name__ == '__main__':
    main()
