import sys
import os


class Directory:

    def __init__(self, name: str):
        self.name = name
        self.files = list()
        self.dirs = list()

    # тут должен был быть еще один перегруженный конструктор но он пал жертвой питона

    def add_file(self, file: str):
        self.files.append(file)

    def add_dir(self, dir):
        self.dirs.append(dir)

    # Print all by depth search
    def print(self, depth=0):
        spacer = " -" * depth
        print(spacer, self.name)
        for file_name in self.files:
            print(spacer, " - ", file_name, sep='')
        for directory in self.dirs:
            directory.print(depth + 1)

    # Set lists files and dirs to object
    # work like depth search for dirs
    def parse(self):
        for name in os.listdir(self.name):
            new_name = os.path.join(self.name, name)
            if os.path.isdir(new_name):
                new_dir = Directory(new_name)
                self.dirs.append(new_dir)
                new_dir.parse()
            else:
                self.files.append(name)


def main(args: list):
    root_dir_name = args[1]
    root_dir = Directory(root_dir_name)

    root_dir.parse()
    root_dir.print()


if __name__ == '__main__':
    main(["main.py", "."])  # Just little test
    main(sys.argv)
