import sys
from config_reader import MoveConfig
from file_property_reader import FileMetadata
from interpreter import Interpreter


def get_new_file_location(file):
    configuration = MoveConfig()
    file_data = FileMetadata(file)
    interpreter = Interpreter(file_properties=file_data.get_file_properties(),
                              move_config=configuration.get_properties(),
                              commands=configuration.get_commands())
    return interpreter.parse_command()


def main():
    print(get_new_file_location(sys.argv[1]))


if __name__ == '__main__':
    main()
