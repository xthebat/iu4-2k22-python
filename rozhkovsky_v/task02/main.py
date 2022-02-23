import sys
import os


class Directory:

    def __init__(self, name: str):
        self.name = name
        self.files = list()
        self.dirs = list()


# Print all by depth search
# step - вложенность(не придумал как это лучше по английски назвать, вся надежда на ревью)
def print_all_rec(root_dir: Directory, step=0):
    spacer = " -" * step
    print(spacer, root_dir.name)
    for file_name in root_dir.files:
        print(spacer, " - ", file_name, sep='')
    for directory in root_dir.dirs:
        print_all_rec(directory, step + 1)


# Set lists files and dirs to object
# work like depth search for dirs
def set_dirs_rec(root_dir: Directory):
    for name in os.listdir(root_dir.name):
        new_name = root_dir.name + "/" + name
        if os.path.isdir(new_name):
            new_dir = Directory(new_name)
            root_dir.dirs.append(new_dir)
            set_dirs_rec(new_dir)
        else:
            root_dir.files.append(name)


def main(args: list):
    root_dir_name = args[1]
    root_dir = Directory(root_dir_name)

    set_dirs_rec(root_dir)
    print_all_rec(root_dir)


if __name__ == '__main__':
    main(["main.py", "."])  # Just little test
    main(sys.argv)
