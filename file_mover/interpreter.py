class Interpreter:

    def __init__(self, file_properties: dict, move_config: dict, commands: list):
        self.file_properties = file_properties
        self.config = move_config
        self.commands = commands

    # This method returns the path of the first command whose antecedent is true
    def parse_command(self) -> str:
        for command in self.commands:
            antecedent, consequent = command.popitem()
            if self.antecedent_corresponds(antecedent):
                return self.get_corresponding_path(consequent)

    # This method returns true if all tokens in an antecedent are true (which are connected by conjunction)
    def antecedent_corresponds(self, antecedent: str) -> bool:
        corresponds = True
        tokens = antecedent.split("&")
        for token in tokens:
            corresponds = self.token_corresponds(token.strip()) & corresponds
        return corresponds

    # This method returns true if the parameter of the given token has a pattern that is contained in the
    # file property of the parameter
    def token_corresponds(self, token: str) -> bool:
        # Gets the left side of the token e.g. the parameter of NAME(hello) is NAME
        parameter = token[0:token.find("(")]
        # Gets the content inside the brackets of a content e.g. the key of NAME(hello) is hello
        key = token[token.find("(") + 1:token.find(")")]

        # config_dic contains all pattern:path pairs of the token-parameter saved in the config.json
        config_dic: dict = self.config.get(parameter)
        # file_property is the value of a parameter which the actual file has
        file_property: str = self.file_properties.get(parameter)
        assert config_dic is not None
        assert file_property is not None

        if key == "*":  # * is a special character which indicates all pattern:path pairs of a parameter
            for pattern in config_dic:  # TODO: Enable usage of glob
                if pattern in file_property:
                    return True  # There has been a match with any pattern of config_dic
        elif key in file_property:
            return True  # The key matches with the property the file has
        return False

    def get_corresponding_path(self, token) -> str:
        parameter = token[0:token.find("(")]
        key = token[token.find("(") + 1:token.find(")")]
        config_dic: dict = self.config.get(parameter)
        file_property: str = self.file_properties.get(parameter)
        assert config_dic is not None
        assert file_property is not None
        if key == "*":
            for pattern in config_dic:
                if pattern in file_property:
                    return config_dic.get(pattern)
        else:
            return config_dic.get(key)
