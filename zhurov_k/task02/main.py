import sys
import os


def dig_tree_dir(dir_str: str) -> list:
    tree = []
    directory = sorted(os.listdir(dir_str))

    for index in directory:
        tree.append(index)
        if os.path.isdir(os.path.join(dir_str, index)):
            add_dir = dig_tree_dir(os.path.join(dir_str, index))
            if add_dir:
                tree.append(add_dir)

    return tree


def print_tree_dir(directory: list, level: int = 0):
    for index in directory:
        if isinstance(index, list):
            print_tree_dir(index, level+1)
        else:
            print("|-" + " - -" * level + "> " + index)


def main(args: list):
    if len(args) == 2:
        directory_name = args[1]
    else:
        directory_name = "./"
    print("Searing in:", directory_name)
    tree_list = dig_tree_dir(directory_name)
    print_tree_dir(tree_list)


if __name__ == '__main__':
    main(sys.argv)
