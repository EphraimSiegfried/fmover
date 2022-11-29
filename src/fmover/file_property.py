import os
import subprocess
import sys


class FileMetadata:
    """
    This class is used to get the file properties of a file.

    Attributes:
        file (str): The path to the file

    Methods:
        get_file_name_with_extension(): Returns the file name with the extension and without the path
        get_file_extension(): Returns the file extension
        get_file_name(): Returns the file name without the extension and without the path
        get_where_from(): Returns the source where the file was obtained from. If nothing is found, it returns "UNKNOWN"
        get_file_properties(): Returns a dictionary of the file properties "WHERE_FROM", "NAME", "FILE_EXTENSION"
    """

    def __init__(self, file: str):
        self.file = file

    def get_file_name_with_extension(self):
        """
        :return: the file name with the extension and without the path
        """
        return os.path.basename(self.file)

    def get_file_extension(self) -> str:
        """
        :return: the file extension
        """
        return os.path.splitext(self.file)[1]

    def get_file_name(self) -> str:
        """
        :return: the file name without the extension and without the path
        """
        return self.get_file_name_with_extension().split(".")[0]

    def get_where_from(self) -> str:
        """
        :return: the source where the file was obtained from. If nothing is found, it returns "UNKNOWN"
        """
        # TODO: This does only work on macos. Make it work on windows and linux
        if sys.platform == "darwin":
            try:
                where_from = subprocess.check_output(["mdls", "-name", "kMDItemWhereFroms", self.file]).decode().split("=")[1].strip()
                return where_from if where_from != "(null)" else "UNKNOWN"
            except subprocess.CalledProcessError:
                raise FileNotFoundError(f"Could not read where the file {self.file} was obtained from")
        return "UNKNOWN"

    def get_file_properties(self) -> dict:
        """
        :return: a dictionary of the file properties "WHERE_FROM", "NAME", "FILE_EXTENSION"
        """
        return {"WHERE_FROM": self.get_where_from(),
                "NAME": self.get_file_name(),
                "FILE_EXTENSION": self.get_file_extension()}
