
import sys
import os


def print_tree(list_tree: list, int_level: int):
    print_str = "\t" * int_level + list_tree[0]
    print(print_str)
    for i in range(1, len(list_tree)):
        if type(list_tree[i]) == list:
            print_tree(list_tree[i], int_level + 1)
        else:
            print_str = "\t" * (int_level + 1) + list_tree[i]
            print(print_str)


def generate_tree(str_dir: str):
    list_cont = os.listdir(str_dir)
    if len(list_cont) > 0:
        list_result = [os.path.basename(str_dir)]
        for item in list_cont:
            item_cond = os.path.join(str_dir, item)
            if os.path.isdir(item_cond):
                next_dir = os.path.join(str_dir, item)
                list_result.append(generate_tree(next_dir))
            else:
                list_result.append(item)
        return list_result
    else:
        return os.path.basename(str_dir)


def main(args: list):

    if len(args) != 2:
        sys.exit("Invalid parameters")

    if not os.path.exists(args[1]):
        sys.exit("Invalid path: directory is not exist")

    if not os.path.isdir(args[1]):
        sys.exit("Invalid path: is not directory")

    result = generate_tree(args[1])
    print_tree(result, 0)


if __name__ == '__main__':
    main(sys.argv)

