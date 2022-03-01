import sys
import os


def generation(directory: str):
    sort_dir = sorted(os.listdir(directory))
    tree_string = []
    for element in sort_dir:
        if os.path.isdir(os.path.join(directory, element)):
            tree_string.append(element)
            if generation(os.path.join(directory, element)):
                tree_string.append(generation(os.path.join(directory, element)))
    return tree_string


def drawing(tree: list, level: int):
    for index in tree:
        if isinstance(index, list):
            drawing(index, level+1)
        else:
            print("|_"+"__" * level + ">" + index)


def main(args: list):
    result = generation(args[1])
    drawing(result, 0)


if __name__ == '__main__':
    main(['main.py', '/Users/obri/Documents/repos/'])
