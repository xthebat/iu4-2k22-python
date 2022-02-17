import sys
import re

# set this to 1 for test mode
test = 1 # like macros define :)


# Shift word on key and print result
def print_cesar(word: str, key: int):
    letters_uppercase = list("ABCDEFGHIJKLMOPQRSTUVWXYZ")
    letters_lowercase = list("abcdefghijklmnopqrstuvwxyz")
    nums = list("0123456789")

    for char in word:
        if str.isnumeric(char):
            index_of_char = nums.index(char)
            real_shift = (index_of_char + key) % 10
            char = nums[real_shift]
        elif str.islower(char):
            index_of_char = letters_lowercase.index(char)
            real_shift = (index_of_char + key) % 26
            char = letters_lowercase[real_shift]
        else:  # str.isupper(char)
            index_of_char = letters_uppercase.index(char)
            real_shift = (index_of_char + key) % 26
            char = letters_uppercase[real_shift]
        print(char, end="")
    print()


def main(args: str):
    regex_res = re.search(r"\A([d|e]) (\w+) (\d+)\Z", args)

    if regex_res is None:
        print("Invalid arguments!", file=sys.stderr)
        if test:
            return 1 # чтобы тесты не вылетели
        else:
            sys.exit(-1)

    crypt = regex_res.group(1)  # d or e
    word = regex_res.group(2)
    key = int(regex_res.group(3))

    if crypt == "e":
        print_cesar(word, key)
    else:
        print_cesar(word, -1 * key)


if __name__ == '__main__':
    if test:
        main("e Cesar123 5")
        main("d Hjxfw678 5")
        main("e ABCDefg155 666")
        main("x Afdsfs1 532")
        main("e AbcDef123!@$#!&$ 54")
        main("e ABCDef123 54!@#")
    else:
        main(" ".join(sys.argv[1:]))
