from os.path import basename
from pathlib import Path
from typing import List

EMPTY = ""
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class Printable:

    def print(self, prefix: str = EMPTY, elbow: str = EMPTY):
        raise NotImplementedError


class File(Printable):

    def __init__(self, name: str):
        self.name = name

    def print(self, prefix: str = EMPTY, elbow: str = EMPTY):
        print(f"{prefix}{elbow} {self.name}")

    def __repr__(self):
        return f"File({self.name})"


class Directory(Printable):
    """Class implementing directory tree"""

    @classmethod
    def from_path(cls, path: Path) -> "Directory":
        directory = Directory(basename(str(path)))
        for file in sorted(path.iterdir()):
            if file.is_dir():
                internal_dir = Directory.from_path(file)
                directory.add(internal_dir)
            else:
                directory.add(File(file.name))
        return directory

    def __init__(self, name: str):
        self.name = name
        self.items: List[Printable] = list()

    def add(self, item: Printable):
        self.items.append(item)

    def print(self, prefix: str = EMPTY, elbow: str = EMPTY):
        if elbow == EMPTY:
            addon = EMPTY
            print(self.name)
        else:
            addon = SPACE_PREFIX if elbow == ELBOW else PIPE_PREFIX
            print(f"{prefix}{elbow} {self.name}")

        for item in self.items[:-1]:
            item.print(prefix=f"{prefix}{addon}", elbow=TEE)

        if len(self.items) > 0:
            self.items[-1].print(prefix=f"{prefix}{addon}", elbow=ELBOW)

    def __repr__(self):
        return f"Directory({self.name})"


def main(args: List[str]):
    directory = Directory.from_path(Path(args[1]))
    directory.print()


if __name__ == '__main__':
    main(["main.py", "."])
