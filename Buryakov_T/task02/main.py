import sys
import os


def dir_tree(start_dir: str) -> list:
    os.chdir(start_dir)
    dir_collection = []
    for name in os.listdir('.'):
        if os.path.isdir(name):
            dir_collection.append(name)
            temp_dir = dir_tree(name)
            if temp_dir:
                dir_collection.append(temp_dir)
    os.chdir("..")
    return dir_collection


def tree_visualization(dir_collection: list, level: int):
    for directory in dir_collection:
        if type(directory) == list:
            tree_visualization(directory, level+1)
        else:
            print("|" + "--"*level + "> " + directory)


def main(arg):
    if arg[2] == 'up':
        while not os.path.isdir(arg[1]):
            os.chdir("..")
    elif arg[2] == 'down':
        while not os.path.isdir(arg[1]):
            os.chdir(".")
    else:
        exit("Unexpected value")
    tree_visualization(dir_tree(arg[1]), 1)


if __name__ == '__main__':
    main(sys.argv)
    # Указывайте директорию выше расположения файла
