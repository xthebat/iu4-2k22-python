import os
import sys


def main(args: list):
    if len(args) == 0:
        directory_name = '.'
    else:
        directory_name = args[0]
    tree_list = generate_tree_list(directory_name)
    print_tree_list(tree_list)


def generate_tree_list(directory_name: str, include_files: bool = False) -> list:
    items_list = os.listdir(directory_name)
    if not include_files:
        items_list = [item for item in items_list if os.path.isdir(os.path.join(directory_name, item))]
    for index in range(len(items_list)):
        item_path = os.path.join(directory_name, items_list[index])
        if os.path.isdir(item_path):
            items_list[index] = generate_tree_list(item_path)

    tree_list = [os.path.split(directory_name)[-1]]
    tree_list.extend(items_list)
    return tree_list[0] if len(tree_list) == 1 else tree_list


def print_tree_list(tree_list: list, prefix: str = ""):
    directory_name = tree_list[0]
    items = tree_list[1:]
    print(directory_name)
    for index, item in enumerate(items):
        is_last_item = (index + 1) == len(items)
        if type(item) == list:
            prefix_addon = "╘═══" if is_last_item else "╞═══"
            print(prefix + prefix_addon, end="")
            print_tree_list(item, prefix + ("    " if is_last_item else "│   "))
        else:
            prefix_addon = "└───" if is_last_item else "├───"
            print(prefix + prefix_addon, item, sep="")


if __name__ == "__main__":
    main(sys.argv[1:])
