import sys
import os


def walk_dir(directory: str):
    sort_dir = sorted(os.listdir(directory))
    tree_string = []
    for element in sort_dir:
        next_dir = os.path.join(directory, element)
        if os.path.isfile(next_dir):
            tree_string.append(element)
        elif os.path.isdir(next_dir):
            tree_string.append(element)
            if walk_dir(next_dir):
                tree_string.append(walk_dir(next_dir))
    return tree_string


def print_tree(tree: list, level: int = 0):
    for index in tree:
        if isinstance(index, list):
            print_tree(index, level+1)
        else:
            print("|-"+"-" * level + ">" + index)


def main(args: list):
    result = walk_dir(args[1])
    print_tree(result, 0)


if __name__ == '__main__':
    main(['main.py', '../'])
