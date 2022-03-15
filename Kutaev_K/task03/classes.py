class FileExtensionError(Exception):
    def __init__(self, true_extension: str, file: str):
        self.true_extension: str = true_extension
        self.file: str = file


class FileContentError(Exception):
    def __init__(self, file: str, line: int):
        self.file: str = file
        self.line: int = line
