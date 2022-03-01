import os
import sys


def collect(current_dir: str):
    os.chdir(current_dir)
    list_of_dirs = [current_dir]
    only_dirs = []
    everything = os.listdir(".")
    if len(everything) != 0:
        for elem in everything:
            if os.path.isdir(everything[everything.index(elem)]):
                only_dirs.append(everything[everything.index(elem)])
        for elem in only_dirs:
            list_of_dirs.append(collect(elem))
    os.chdir("..")
    return list_of_dirs


def print_list_of_dirs(directory: list, lev: int = 0):  # Функция печати аккуратно скопирована и исправлена
    for index in directory:
        if isinstance(index, list):
            print_list_of_dirs(index, lev + 1)
        else:
            print("|" + " |" * lev + " |> " + index)


def main(args: list):
    while not os.path.isdir(args[1]):
        os.chdir("..")
    print_list_of_dirs(collect(args[1]))


if __name__ == '__main__':
    main(sys.argv)
