import sys
import os

current_dir_signs = ["", " ", "."]


# 'stdin' arguments check
def arg_check(args: list) -> str:
    # Check the number of given arguments
    if len(args) > 1:
        sys.exit("There must be only one argument - path of root directory")
    # Check the validity of an argument
    elif not isinstance(args[0], str):
        sys.exit("'stdin' can receive only strings as arguments")
    # If above checks are passed
    else:
        # Return the name of the current directory
        if args[0] in current_dir_signs:
            return os.getcwd()
        # Otherwise, check the existence of the given directory
        return args[0] if os.path.isdir(args[0]) else sys.exit("There's no such directory")


# Returns list of nested first-level directories of given root
def get_nested_dirs(given_root: str) -> list:
    nested_files = os.listdir(given_root)
    if nested_files:
        dirs_in_nest = []
        # Check if received values are directories
        is_dir_values = list(map(os.path.isdir, [given_root + "\\" + file_name for file_name in nested_files]))
        for is_dir, file_name in zip(is_dir_values, nested_files):
            if is_dir:
                dirs_in_nest.append(file_name)
        return dirs_in_nest
    else:
        return []


# Example of compiling structure:
# {'dir1': [{'dir11': ['dir11_1', 'dir11_2']}, 'dir12', {'dir13': 'dir13_1'}, {'dir14': [{'dir15_2': 'dir15_2-1'}]}]}
def fill_tree(root: str, tree: dict) -> int:
    # Dict key   - root directory;
    # Dict value - subdirectories
    tree[root] = get_nested_dirs(root)
    if tree[root]:  # If it has any subdirectories
        for index, sub_dir in enumerate(tree[root]):
            # Make subdirectory a new root
            new_root = root + "\\" + sub_dir
            flag = fill_tree(new_root, {})
            if flag == 1:
                tree[root][index] = {sub_dir: get_nested_dirs(new_root)}
        return 1
    else:
        return -1


# Only root directory is presented in "absolute form"
# Other directories are related to root one
def print_tree(tree: dict, nest_depth: int) -> None:
    for root, branch in tree.items():
        print(" " * 4 * nest_depth + f'{root}')
        nest_depth += 1
        for item in branch:
            if type(item) is dict:
                print_tree(item, nest_depth)
            else:
                print(" " * 4 * nest_depth + f'{item}')
    return None


def main(args: list) -> None:
    start_point = arg_check(args)
    start_depth = 0
    full_path = dict()

    # Fill with a content
    fill_tree(start_point, full_path)
    # Print the result
    print('---------------------')
    print_tree(full_path, start_depth)
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(["."])
    #main(["C:\\Users"])
    #main(["C:\\Users\\DELL\\Desktop"])
