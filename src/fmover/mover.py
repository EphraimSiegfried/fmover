import shutil
from os import listdir, getcwd, path, mkdir
from os.path import isfile, join, isabs, normpath, exists, dirname, isdir, relpath
import notifypy
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
        try:
            self.configuration = MoveConfig(move_config_path)
            self.configuration.validate_config()
        except ValueError as e:
            logger.error(f"Could not interpret configuration: {e}")
            exit(1)

    def _get_new_file_location(self, file_data: FileMetadata) -> str:
        interpreter = Interpreter(
            file_properties=file_data.get_file_properties(),
            move_config=self.configuration.get_properties(),
            commands=self.configuration.get_commands(),
        )
        location = interpreter.parse_command()
        if location is None:
            location = dirname(file_data.file)
        return join(location, file_data.get_file_name_with_extension())

    def _notify(self, file_name, new_location) -> None:
        notification = notifypy.Notify()
        notification.application_name = "File has been moved"
        notification.title = file_name
        notification.message = new_location
        notification.send()

    def move_file(
        self,
        file_path: str,
        should_notify: bool = False,
        force: bool = False,
        dry_run: bool = False,
    ) -> None:
        """
        Moves a file to a new location based on the configuration file
        :param force: If true, the destination directory will be created if it does not exist
        :param file_path: The path of the file (can be a relative path)
        :param should_notify: If True, a pop-up notification will be shown
        :param dry_run: If true, the file will not be moved
        """
        file_data = FileMetadata(file_path)
        logger.debug(f"File data: {file_data.get_file_properties()}")
        new_file_path = self._get_new_file_location(file_data)
        if not isabs(new_file_path):
            new_file_path = normpath(join(dirname(file_path), new_file_path))
        f_name = file_data.get_file_name_with_extension()
        dir_of_new_file = path.dirname(new_file_path)
        if file_path == new_file_path:
            logger.info(f"No change: {f_name}")
            return

        if not exists(dir_of_new_file) and force:
            mkdir(dir_of_new_file)
        elif not exists(dir_of_new_file):
            logger.warning(
                f"The destination directory does not exist: {dir_of_new_file} "
                f"\n if you wish to create directories if they do not exist, "
                f"please add the -f flag"
            )
            return
        if exists(new_file_path):
            logger.warning(
                f"A file with the same name already exists in the destination directory: {new_file_path}"
            )
            return
        if not dry_run:
            shutil.move(file_path, new_file_path)
        if should_notify:
            self._notify(f_name, new_file_path)
        logger.info(f"Moved: {relpath(new_file_path, file_path)}")
        logger.debug(f"Moved: {normpath(file_path)} -> {new_file_path}")

    def move_files_in_dir(
        self,
        path_to_directory: str,
        should_notify: bool = False,
        force: bool = False,
        dry_run: bool = False,
    ) -> None:
        """
        Moves all files in a directory to a new location based on the configuration file
        :param force: If true, the destination directory will be created if it does not exist
        :param path_to_directory: The path of the directory
        :param should_notify: If True, a pop-up notification will be shown
        :param dry_run: If true, the files will not be moved
        """
        if not isabs(path_to_directory):
            path_to_directory = join(getcwd(), path_to_directory)
        file_paths = [
            join(path_to_directory, file)
            for file in listdir(path_to_directory)
            if file[0] != "." and isfile(join(path_to_directory, file))
        ]
        for file_path in file_paths:
            self.move_file(file_path, should_notify, force, dry_run)
