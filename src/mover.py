import shutil
import os
from notifypy import Notify
from src.config import MoveConfig
from src.file_property import FileMetadata
from src.interpreter import Interpreter


class Mover:

    def __init__(self, move_config_path):
        self.configuration = MoveConfig(move_config_path)

    def _get_new_file_location(self, file_data: FileMetadata) -> str:
        interpreter = Interpreter(file_properties=file_data.get_file_properties(),
                                  move_config=self.configuration.get_properties(),
                                  commands=self.configuration.get_commands())
        location = interpreter.parse_command()
        if location is None:
            location = os.path.dirname(file_data.file)
        return os.path.join(location, file_data.get_file_name_with_extension())

    def _notify(self, file_name, new_location) -> None:
        notification = Notify()
        notification.application_name = "File has been moved"
        notification.title = file_name
        notification.message = new_location
        notification.send()

    def move_file(self, file_path: str, should_notify: bool):
        file_data = FileMetadata(file_path)
        new_file_path = self._get_new_file_location(file_data)
        if not os.path.isabs(new_file_path):
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_path)

        f_name = file_data.get_file_name_with_extension()
        if not os.path.exists(new_file_path):
            shutil.move(file_path, new_file_path)
            print(f"{'File successfully moved:':<25}",os.path.relpath(new_file_path, file_path))
        elif file_path == new_file_path:
            print(f"{'No match with command:': <25}",f_name)
        else:
            print(f"{'File with same name already exists in destination folder:': .<25}", f_name)
        if should_notify and file_path != new_file_path:
            self._notify(file_data.get_file_name_with_extension(), new_file_path)

    def move_files_in_dir(self, path_to_directory: str, should_notify: bool):
        file_paths = [os.path.join(path_to_directory, file) for file in os.listdir(path_to_directory)]
        for file_path in file_paths:
            if not os.path.isdir(file_path):
                self.move_file(file_path, should_notify)
