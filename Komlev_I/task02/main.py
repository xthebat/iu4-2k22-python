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
    tree_string = []
    for index in range(level):
        tree_string.append("_")
    print("|", "".join(tree_string)+tree[0])
    tree_string.append("_")
    for index in range(len(tree)-1):
        if type(tree[index+1]) != list:
            print('|', "".join(tree_string) + tree[index])
        else:
            drawing(tree[index + 1], level + 1)


def main(args: list):
    result = generation(args[1])
    drawing(result, 0)


if __name__ == '__main__':
    main(['main.py', '.'])
    