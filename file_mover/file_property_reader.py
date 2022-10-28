from osxmetadata import OSXMetaData
import pathlib


class FileMetadata:

    def __init__(self, file):
        self.file = file

    def get_file_extension(self):
        return pathlib.Path(self.file).suffix

    def get_file_name(self):
        return pathlib.Path(self.file).name

    def get_where_from(self):
        print(self.file)
        return OSXMetaData(self.file).get("kMDItemWhereFroms")

    def get_file_properties(self):
        return {"WHERE_FROM": self.get_where_from(),
                "NAME": self.get_file_name(),
                "FILE_EXTENSION": self.get_file_extension()}

