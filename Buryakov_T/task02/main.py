import sys
import os


def dir_tree(start_dir: str) -> list:
    dir_collection = []
    for name in sorted(os.listdir(start_dir)):
        if os.path.isdir(os.path.join(start_dir, name)):
            dir_collection.append(name)
            dir_collection.append(dir_tree(os.path.join(start_dir, name)))
        else:
            dir_collection.append(name)
    return dir_collection


def tree_visualization(start_dir: str, dir_collection: list):
    for i, item in enumerate(dir_collection):
        if type(item) == list:
            tree_visualization(start_dir + "--> " + dir_collection[i - 1], item)
        else:
            print(start_dir + "--> " + item)


def main(arg: list):
    tree_visualization(arg[1], dir_tree(arg[1]))


if __name__ == '__main__':
    main(sys.argv)
