from dataclasses import dataclass


@dataclass
class FileExtensionError(Exception):
    true_extension: str
    file: str


@dataclass
class FileContentError(Exception):
    file: str
    line: int
