import sys
import os


def dir_tree(path: str) -> list:
    list_out = []
    dir_list = os.listdir(path)
    for item in dir_list:
        temp = path
        path += '\\' + item
        list_out.append(item)
        if os.path.isdir(path):
            list_out.append(dir_tree(path))
        path = temp
    return list_out


def print_branches(tree: list, depth: int):
    for item in tree:
        if isinstance(item, list):
            print_branches(item, depth + 1)
        else:
            print('-' * depth + item)


def print_tree(tree: list, depth: int, root: str):
    print(root)
    print_branches(tree, depth)


def main(args: list):
    tree = dir_tree(args[1])
    print_tree(tree, 1, args[1])


if __name__ == '__main__':
    main(sys.argv)

