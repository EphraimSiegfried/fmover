import shutil
import os
import notifypy as notify
from fmover.config import MoveConfig
from fmover.file_property import FileMetadata
from fmover.interpreter import Interpreter


class Mover:

    def __init__(self, move_config_path):
        self.configuration = MoveConfig(move_config_path)
        self.configuration.validate_config()

    def _get_new_file_location(self, file_data: FileMetadata) -> str:
        interpreter = Interpreter(file_properties=file_data.get_file_properties(),
                                  move_config=self.configuration.get_properties(),
                                  commands=self.configuration.get_commands())
        location = interpreter.parse_command()
        if location is None:
            location = os.path.dirname(file_data.file)
        return os.path.join(location, file_data.get_file_name_with_extension())

    def _notify(self, file_name, new_location) -> None:
        notification = notify.Notify()
        notification.application_name = "File has been moved"
        notification.title = file_name
        notification.message = new_location
        notification.send()

    def move_file(self, file_path: str, should_notify: bool) -> None:
        """
        Moves a file to a new location based on the configuration file
        :param file_path: The path of the file (can be a relative path)
        :param should_notify: If True, a notification will be shown
        """
        file_data = FileMetadata(file_path)
        new_file_path = self._get_new_file_location(file_data)
        if not os.path.isabs(new_file_path):
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_path)

        f_name = file_data.get_file_name_with_extension()
        dir_of_new_file = os.path.dirname(new_file_path)
        if not os.path.exists(dir_of_new_file):
            raise FileNotFoundError(f"The destination directory {dir_of_new_file} does not exist.")
        if not os.path.exists(new_file_path):
            shutil.move(file_path, new_file_path)
            if should_notify:
                self._notify(file_data.get_file_name_with_extension(), new_file_path)
            print(f"{'File successfully moved:':<25}", os.path.relpath(new_file_path, file_path))
        elif file_path == new_file_path:
            print(f"{'No match with command:':<25}", f_name)
        else:
            print(f"{'File with same name already exists in destination folder:': <25}", f_name)

    def move_files_in_dir(self, path_to_directory: str, should_notify: bool) -> None:
        """
        Moves all files in a directory to a new location based on the configuration file
        :param path_to_directory: The path of the directory
        :param should_notify: If True, a notification will be shown
        """
        if not os.path.isdir(path_to_directory):
            raise FileNotFoundError(f"The directory {path_to_directory} does not exist.")
        file_paths = [os.path.join(path_to_directory, file) for file in os.listdir(path_to_directory) if file[0] != "."
                      and os.path.isfile(os.path.join(path_to_directory, file))]
        for file_path in file_paths:
            self.move_file(file_path, should_notify)
