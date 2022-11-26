import shutil
from os import listdir, getcwd, path, mkdir
from os.path import isfile, join, isabs, normpath, exists, dirname, isdir, relpath
import notifypy as notify
from fmover.config import MoveConfig
from fmover.file_property import FileMetadata
from fmover.interpreter import Interpreter
from fmover.base_logger import logger


class Mover:
    """
    This class is responsible for moving files to a new location based on a configuration file.

    Attributes:
        configuration (MoveConfig): A MoveConfig object that represents the configuration file

    Methods:
        move_file(file_path: str, should_notify: bool) -> None
            Moves a file to a new location based on the configuration file
        move_files_in_dir(path_to_directory: str, should_notify: bool) -> None
            Moves all files in a directory to a new location based on the configuration file
    """

    def __init__(self, move_config_path: str):
        self.configuration = MoveConfig(move_config_path)
        self.configuration.validate_config()

    def _get_new_file_location(self, file_data: FileMetadata) -> str:
        interpreter = Interpreter(file_properties=file_data.get_file_properties(),
                                  move_config=self.configuration.get_properties(),
                                  commands=self.configuration.get_commands())
        location = interpreter.parse_command()
        if location is None:
            location = dirname(file_data.file)
        return join(location, file_data.get_file_name_with_extension())

    def _notify(self, file_name, new_location) -> None:
        notification = notify.Notify()
        notification.application_name = "File has been moved"
        notification.title = file_name
        notification.message = new_location
        notification.send()

    def move_file(self, file_path: str, should_notify: bool, force: bool) -> None:
        """
        Moves a file to a new location based on the configuration file
        :param force: If true, the destination directory will be created if it does not exist
        :param file_path: The path of the file (can be a relative path)
        :param should_notify: If True, a pop-up notification will be shown
        """
        file_data = FileMetadata(file_path)
        logger.debug(f"File data: {file_data.get_file_properties()}")
        new_file_path = self._get_new_file_location(file_data)
        if not isabs(new_file_path):
            new_file_path = normpath(join(dirname(file_path), new_file_path))
        f_name = file_data.get_file_name_with_extension()
        dir_of_new_file = path.dirname(new_file_path)
        if file_path == new_file_path:
            logger.info(f"The file is already in the correct location: {f_name}")
            return

        if not exists(dir_of_new_file) and force:
            mkdir(dir_of_new_file)
        elif not exists(dir_of_new_file):
            logger.warning(f"The destination directory does not exist: {dir_of_new_file} ")
            return
        if exists(new_file_path):
            logger.warning(f"A file with the same name already exists in the destination directory: {new_file_path}")
            return

        shutil.move(file_path, new_file_path)
        if should_notify:
            self._notify(file_data.get_file_name_with_extension(), new_file_path)
        logger.info(f"File successfully moved: {relpath(new_file_path, file_path)}")
        logger.debug(f"File successfully moved: {normpath(file_path)} -> {new_file_path}")

    def move_files_in_dir(self, path_to_directory: str, should_notify: bool, force: bool) -> None:
        """
        Moves all files in a directory to a new location based on the configuration file
        :param force: If true, the destination directory will be created if it does not exist
        :param path_to_directory: The path of the directory
        :param should_notify: If True, a pop-up notification will be shown
        """
        if not isabs(path_to_directory):
            path_to_directory = join(getcwd(), path_to_directory)
        if not isdir(path_to_directory):
            raise FileNotFoundError(f"The directory {path_to_directory} does not exist.")
        file_paths = [join(path_to_directory, file) for file in listdir(path_to_directory) if file[0] != "."
                      and isfile(join(path_to_directory, file))]
        for file_path in file_paths:
            self.move_file(file_path, should_notify, force)
