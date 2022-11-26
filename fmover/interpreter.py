from fmover.base_logger import logger


def _get_parameter(token: str) -> str:
    """
    :param token: a token of the form "PARAMETER(PATTERN)"
    :return: the parameter of the token
    """
    return token[0:token.find("(")].strip()


def _get_pattern(token: str) -> str:
    """
    :param token: a token of the form "PARAMETER(PATTERN)"
    :return: the pattern of the token
    """
    return token[token.find("(") + 1:token.find(")")].strip()


class Interpreter:
    """
    This class compares file properties with configuration properties based on commands.

    Example:
    file_properties = {"WHERE_FROM": "https://www.google.com", "NAME": "hello", "FILE_EXTENSION": ".txt"}
    move_config = {"WHERE_FROM": {"https://www.google.com": "C:/Users/Downloads/Google", "https://www.youtube.com": "C:/Users/Downloads/Youtube"},
                    "NAME": {"hello": "C:/Users/Downloads/Hello", "world": "C:/Users/Downloads/World"},
                    "FILE_EXTENSION": {".txt": "C:/Users/Downloads/Text", ".pdf": "C:/Users/Downloads/PDF"}}
    commands = [{"WHERE_FROM(https://www.google.com) & NAME(hello)": "NAME(*)"}, {"WHERE_FROM(https://www.youtube.com) & NAME(world)": "NAME(*)"}]

    The Interpreter class will return the path "C:/Users/Downloads/Hello" because the antecedent of the first command is true.

    Attributes:
        file_properties: A dictionary of file properties
        config: A dictionary of configuration properties
        commands: A list of commands

    Methods:
        parse_command: Returns the path of the first command whose antecedent is true
        antecedent_corresponds: Returns true if all tokens in an antecedent are true (which are connected by conjunction)
        token_corresponds: Returns true if the parameter of the given token has a pattern that is contained in the
                           file property of the parameter
        get_corresponding_path: Returns the path of the command whose antecedent is true
    """

    # Dictionary:
    # Antecedent: The left side of a command
    # Consequent: The right side of a command
    # Token: The part of an antecedent which is separated by conjunction
    # Parameter: The left side of a token e.g. the parameter of NAME(hello) is NAME
    # Pattern: The content inside the brackets of a token e.g. the pattern of NAME(hello) is hello
    # Property: A configuration property e.g. Name, File Extension, Where From
    # *: A wildcard which indicates all pattern:path pairs of a parameter

    def __init__(self, file_properties: dict, move_config: dict, commands: list):
        self.file_properties = file_properties
        self.config = move_config
        self.commands = commands

    def parse_command(self) -> str:
        """
        :return: The path of the first command whose antecedent is true
        """
        for command in self.commands:
            (antecedent, consequent), = command.items()
            if self.__antecedent_corresponds(antecedent):
                logger.debug(f"Executed command: {command}")
                return self.__get_corresponding_path(consequent)

    def __antecedent_corresponds(self, antecedent: str) -> bool:
        """
        :param antecedent: The antecedent of a command
        :return: True if all tokens in an antecedent are true (which are connected by conjunction)
        """
        return all(self.__token_corresponds(token.strip()) for token in antecedent.split("&"))

    # This method returns true if the parameter of the given token has a pattern that is contained in the
    # file property of the parameter
    def __token_corresponds(self, token: str) -> bool:
        """
        :param token: The token of an antecedent
        :return: True if the parameter of the given token has a pattern that
        is contained in the file property of the parameter
        """
        parameter, pattern = _get_parameter(token), _get_pattern(token)
        property_dic: dict = self.config.get(parameter)
        file_property: str = self.file_properties.get(parameter)
        if parameter not in self.file_properties:
            raise ValueError(f"The parameter and property {parameter} is not supported by the program")
        if pattern == "*":
            return any(property_pattern in file_property for property_pattern in property_dic)
        elif pattern in file_property:
            return True
        return False

    def __get_corresponding_path(self, token: str) -> str:
        """
        :param token: The consequent of a command
        :return: The path of the command whose antecedent is true
        """
        parameter, pattern = _get_parameter(token), _get_pattern(token)
        property_dic: dict = self.config.get(parameter)
        if parameter not in self.file_properties:
            raise ValueError(f"The parameter and property {parameter} is not supported by the program")
        if pattern == "*":
            for parameter_pattern in property_dic:
                if parameter_pattern in self.file_properties.get(parameter):
                    return property_dic.get(parameter_pattern)
        else:
            return property_dic.get(pattern)
