import os
import sys


def collect(current_dir: str):
    list_of_dirs = [current_dir.split("/")[-1]]
    everything = os.listdir(current_dir)
    if len(everything) != 0:
        for index, elem in enumerate(everything):
            list_of_dirs.append(elem)
            if os.path.isdir(os.path.join(current_dir, elem)):
                list_of_dirs.append(collect(os.path.join(current_dir, elem)))
    return list_of_dirs


def print_list_of_dirs(directory: list, lev: int = 0):
    for index in directory:
        if isinstance(index, list):
            print_list_of_dirs(index, lev + 1)
        else:
            print("|" + " |" * lev + " |> " + index)


def main(args: list):
    print_list_of_dirs(collect(args[1]))


if __name__ == '__main__':
    main(sys.argv)
