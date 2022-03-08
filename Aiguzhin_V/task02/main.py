import sys
import os


# 'stdin' arguments check
def arg_check(args: list) -> str:
    if len(args) > 1:
        sys.exit("There must be only one argument - path of root directory")
    else:
        # Return the name of the current directory
        if not args:
            return os.getcwd()
        # Otherwise, check the existence of the given directory
        return os.path.realpath(args[0]) if os.path.isdir(args[0]) else sys.exit("There's no such directory")


# Return content of the given root
def fill_tree(root: str):
    if os.path.isdir(root):
        nested_files = os.listdir(root)
        full_path = dict()
        if nested_files:
            full_path[root] = dict()
            for file in nested_files:
                abs_path = root + "\\" + file
                full_path[root][file] = fill_tree(abs_path)
            return full_path[root]
        else:
            return None
    else:               # If it's not a directory then nothing can be inside
        return None


# Only root directory is presented in "absolute form"
# Other directories are related to root one
def print_tree(tree: dict, nest_depth=0) -> None:
    for key, value in tree.items():
        print(" " * 4 * nest_depth + f'{key}')
        if value:
            print_tree(value, nest_depth + 1)
    return None


def main(args: list) -> None:
    start_point = arg_check(args)
    final_tree = dict()
    # Fill the tree
    final_tree[start_point] = fill_tree(start_point)
    # Print the result
    print('-' * 25)
    print_tree(final_tree)

    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(["../../../"])
    # main(["C:\\Users"])
    # main(["C:\\Users\\DELL\\Desktop"])
