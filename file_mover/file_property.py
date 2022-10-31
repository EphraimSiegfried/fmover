from osxmetadata import OSXMetaData
import os


class FileMetadata:

    def __init__(self, file):
        self.file = file

    def get_file_name_with_extension(self):
        return self.file.split("/")[-1]

    def get_file_extension(self) -> str:
        return os.path.splitext(self.file.split("/")[-1])[1] if "/" in self.file else os.path.splitext(self.file)

    def get_file_name(self) -> str:
        return os.path.splitext(self.file.split("/")[-1])[0] if "/" in self.file else os.path.splitext(self.file)

    def get_where_from(self) -> str:
        return ''.join(OSXMetaData(self.file).get("kMDItemWhereFroms"))

    def get_file_properties(self) -> dict:
        return {"WHERE_FROM": self.get_where_from(),
                "NAME": self.get_file_name(),
                "FILE_EXTENSION": self.get_file_extension()}