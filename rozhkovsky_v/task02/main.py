import sys
import os
from typing import List, Optional


class Directory:

    # Set lists files and dirs to object
    # work like depth search for dirs
    @classmethod
    def parse(cls, root: str):
        result = cls(root)

        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                result.add_dir(Directory.parse(path))
            else:
                result.add_file(name)

        return result

    def __init__(
            self,
            name: str,
            files: Optional[List[str]] = None,
            dirs: Optional[List["Directory"]] = None
    ):
        self.name = name
        self.files = files or list()
        self.dirs = dirs or list()

    def add_file(self, file: str):
        self.files.append(file)

    def add_dir(self, directory: "Directory"):
        self.dirs.append(directory)

    # Print all by depth search
    def print(self, depth=0):
        spacer = " -" * depth
        print(spacer, self.name)
        for file_name in self.files:
            print(spacer, " - ", file_name, sep='')
        for directory in self.dirs:
            directory.print(depth + 1)


def main(args: List[str]):
    root_dir_name = args[1]
    root_dir = Directory.parse(root_dir_name)

    root_dir.print()


if __name__ == '__main__':
    main(["main.py", "../../"])  # Just little test
    # main(sys.argv)
