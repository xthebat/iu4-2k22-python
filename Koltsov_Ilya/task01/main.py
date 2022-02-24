import sys

CIPHER_DICTIONARY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

#a function, which processes each letter
def move_char(mode: str, char: str, key: int):
    if mode == "d":
        key = -key
#updating the key value to implement a loop-like dictionary behaviour
    if CIPHER_DICTIONARY.index(char) + key > len(CIPHER_DICTIONARY):
        key = key - len(CIPHER_DICTIONARY) - 1
        processed_char = CIPHER_DICTIONARY[key]
    else:
        processed_char = CIPHER_DICTIONARY[CIPHER_DICTIONARY.index(char) + key]
    return processed_char

#Error output
def error(string: str):
    print(string)
    sys.exit(-1)

#Main
def main(args: list):
    mode: str = args[1]
    string: str = args[2]
    key: int = int(args[3])

#Error handlers
    if (mode != "e") & (mode != "d"):
        error("1st argument invalid - \"d\" OR \"e\" expected.")
    if not args[3].isdigit():
        error("The 3rd argument (key) must be a number.")
    if len(args) != 4:
        error("Unable to process more or less than 3 arguments.")

#Processing the input arguments
    char_list: list = list(string)
    res_list: list = []
    for char in char_list:
        res_list.append(move_char(mode, char, key))
    res = "".join(res_list)
    print(res)
    return 0


if __name__ == '__main__':
    main(sys.argv)
