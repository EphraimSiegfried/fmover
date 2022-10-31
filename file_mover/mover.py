import sys
import os
from notifypy import Notify

from config_reader import MoveConfig
from file_property_reader import FileMetadata
from interpreter import Interpreter


def get_new_file_location(file, move_config_path) -> str:
    configuration = MoveConfig(move_config_path)
    file_data = FileMetadata(file)
    interpreter = Interpreter(file_properties=file_data.get_file_properties(),
                              move_config=configuration.get_properties(),
                              commands=configuration.get_commands())
    return interpreter.parse_command()


def notify(file_name, new_location) -> None:
    notification = Notify()
    notification.application_name = "File has been moved"
    notification.title = file_name
    notification.message = new_location
    notification.send()


def main():
    # Get necessary information
    file_location = sys.argv[1]
    file_name = FileMetadata(file_location).get_file_name_with_extension()
    move_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

    # Move file
    new_file_location = get_new_file_location(file_location, move_config_path)
    os.rename(file_location, new_file_location + file_name)

    # Notify user
    notify(file_name, new_file_location)


if __name__ == '__main__':
    main()
