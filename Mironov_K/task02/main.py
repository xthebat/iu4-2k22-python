
import sys
import os


def print_tree(list_tree: list, int_level: int):
    list_level = []
    for i in range(int_level):
        list_level.append("\t")
    print_list = list_level + list(list_tree[0])
    print("".join(print_list))
    list_level.append("\t")
    for i in range(1, len(list_tree)):
        if type(list_tree[i]) == list:
            print_tree(list_tree[i], int_level+1)
        else:
            print_list = list_level + list(list_tree[i])
            print("".join(print_list))


def generate_tree(str_dir: str):
    list_cont = os.listdir(str_dir)
    list_dir = []
    for item in list_cont:
        item_cond = os.path.join(str_dir, item)
        if os.path.isdir(item_cond):
            list_dir.append(item)
    if len(list_dir) > 0:
        list_result = [os.path.basename(str_dir)]
        for item in list_dir:
            next_dir = os.path.join(str_dir, item)
            list_result.append(generate_tree(next_dir))
        return list_result
    else:
        return os.path.basename(str_dir)


def main(args: list):
    if len(args) == 2:
        if os.path.exists(args[1]):
            if os.path.isdir(args[1]):
                result = generate_tree(args[1])
                print_tree(result, 0)
            else:
                sys.exit("Invalid path: is not directory")
        else:
            sys.exit("Invalid path: directory is not exist")
    else:
        sys.exit("Invalid parameters")


if __name__ == '__main__':
    main(sys.argv)

