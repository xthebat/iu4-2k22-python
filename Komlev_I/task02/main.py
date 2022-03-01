import sys
import os


def generation(directory: str):
    sort_dir = sorted(os.listdir(directory))
    tree_string = []
    for element in sort_dir:
        if os.path.isdir(os.path.join(directory, element)):
            tree_string.append(element)
    if tree_string == 0:
        return os.path.basename(directory)
    else:
        final_list = [os.path.basename(directory)]
        for element in tree_string:
            final_list.append(generation(os.path.join(directory, element)))
        return final_list


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
    main(['main.py', '.'])
