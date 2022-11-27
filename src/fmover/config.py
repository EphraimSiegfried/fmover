import json


class MoveConfig:
    """
    This class represents a configuration file.

    A move configuration is a JSON file which consists of a command and properties e.g. NAME, FILE_EXTENSION,
    WHERE_FROM.

    Attributes:
        config: The path of the configuration file or a dictionary which contains the configuration

    Methods:
        get_config: Returns the configuration file as a dictionary
        get_commands: Returns a list of commands
        get_properties: Returns a dictionary of properties
    """

    def __init__(self, config):
        if isinstance(config, str):
            with open(config, "r") as file:
                self.config = json.load(file)
        elif isinstance(config, dict):
            self.config = config
        else:
            raise ValueError(f"The config must be a path (string) or a dictionary")

    def get_commands(self) -> list:
        """
        :return: A list of dictionaries which contains the commands
        """
        return self.config.get("COMMAND")

    def get_properties(self) -> dict:
        """
        :return: A dictionary of dictionaries which contains the properties
        """
        return {key: value for key, value in self.config.items() if key != "COMMAND"}

    def validate_config(self) -> bool:
        """
        A valid config is a dict which must have a key "COMMAND" with a value which is a list of singleton dictionaries.
        These singleton dictionaries are commands which consist of antecedents (as keys) and consequents (as values).
        An antecedent consist of tokens which are seperated by "&". A consequent only has one token.
        Tokens consist of a parameter and a pattern. The tokens have the following form: "PARAMETER(PATTERN)".
        The parameter can be one of the following: "NAME", "FILE_EXTENSION", "WHERE_FROM".
        The pattern can be a string or a wildcard "*".
        If the parameter is declared in the command it must be a property in the config.

        This method raises a ValueError if the config is invalid. It shows where the error occurred
        :return: True if the configuration is valid, otherwise it raises a ValueError
        """

        if "COMMAND" not in self.config:
            raise ValueError(f"The config does not have a key \"COMMAND\"")

        if not isinstance(self.config["COMMAND"], list):
            raise ValueError(f"The value of the key \"COMMAND\" is not a list of dictionaries")

        for command in self.config["COMMAND"]:
            if not isinstance(command, dict):
                raise ValueError(f"The command {command} is not a dictionary")
            if len(command) != 1:
                raise ValueError(f"The command {command} is not a singleton dictionary")

            antecedent, consequent = list(command.items())[0]
            antecedent_tokens = antecedent.split("&")
            consequent_token = consequent

            for token in antecedent_tokens:
                self.__validate_token(token)
            self.__validate_token(consequent_token)
        return True

    def __validate_token(self, token: str):
        if "(" not in token or ")" not in token:
            raise ValueError(
                f"The token {token} is not a valid token. A token must have the form \"PARAMETER(PATTERN)\"")
        parameter, pattern = token.split("(")
        parameter = parameter.strip()
        pattern = pattern.replace(")", "").strip()
        if parameter not in self.config:
            raise ValueError(f"The parameter {parameter} is not declared in the config")
        if pattern != "*" and pattern not in self.config[parameter]:
            raise ValueError(f"The pattern {pattern} is not declared in the config for the parameter {parameter}")
