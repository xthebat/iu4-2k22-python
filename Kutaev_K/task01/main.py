import sys


def move_char(char, key):
    dictionary = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    for symbol in dictionary:
        if symbol == char:
            if dictionary.index(symbol) + int(key) > len(dictionary):
                key = int(key) - len(dictionary) - 1
                movedChar = dictionary[key]
            else:
                movedChar = dictionary[dictionary.index(symbol) + int(key)]
    return movedChar


def main(args: list):
    mode = args[1]
    string = args[2]
    key = args[3]
    resList = []
    i = 0

    # errors
    if (mode != "e") & (mode != "d"):
        return print("Invalid 1 arg")
    if not key.isdigit():
        return print("3 arg must be a number")
    if len(args) != 4:
        return print("Only 3 args")

    charList = list(string)
    for char in charList:
        if mode == "e":
            resList.append(move_char(char, key))
            i += 1
        else:
            resList.append(move_char(char, -int(key)))
            i += 1
    res = "".join(resList)
    print(res)
    return 0


if __name__ == '__main__':
    main(sys.argv)

