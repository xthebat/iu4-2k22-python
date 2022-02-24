import sys

DICTIONARY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def move_char(mode: str, char: str, key: int):
    if mode == "d":
        key = -key
    if DICTIONARY.index(char) + key > len(DICTIONARY):
        key = key - len(DICTIONARY) - 1
        moved_char = DICTIONARY[key]
    else:
        moved_char = DICTIONARY[DICTIONARY.index(char) + key]
    return moved_char


def error(string: str):
    print(string)
    sys.exit(-1)


def main(args: list):
    mode: str = args[1]
    string: str = args[2]
    key: int = int(args[3])


    # errors
    if (mode != "e") & (mode != "d"):
        error("Invalid 1 arg")
    if not args[3].isdigit():
        error("3 arg must be a number")
    if len(args) != 4:
        error("Only 3 args")

    # parse args
    char_list: list = list(string)
    res_list: list = []
    for char in char_list:
        res_list.append(move_char(mode, char, key))
    res = "".join(res_list)
    print(res)
    return 0


if __name__ == '__main__':
    main(sys.argv)

