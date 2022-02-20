import sys
import string
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGIT = string.digits
PUNCT = string.punctuation
ALL_TEXT = string.ascii_letters+DIGIT+PUNCT


def encryption(category: str, char: str, key: int):
    mod_char = category[(category.find(char) + key) % len(category)]
    return mod_char


def check_text(text: str):
    for char in text:
        if char not in ALL_TEXT:
            print(f"Invalid symbol = {char} in input text")
            sys.exit(-1)


def check_key(key: str):
    for char in key:
        if char not in DIGIT:
            print(f"Invalid symbol = {char} in input key")
            sys.exit(-1)


def check_command(action: str):
    if action != "e" and action != "d":
        print(f"Invalid command = {action}")
        sys.exit(-1)


def check_argument(arg: int):
    if arg != 4:
        print("Invalid number of arguments")
        sys.exit(-1)


def ceaser(text: list, key: int):
    for i in range(len(text)):
        if text[i].islower():
            text[i] = encryption(LOWER, text[i], key)
        elif text[i].isupper():
            text[i] = encryption(UPPER, text[i], key)
        elif text[i].isdigit():
            text[i] = encryption(DIGIT, text[i], key)
    return text


def main(args: list):
    check_argument(len(args))
    check_command(str(args[1]))
    check_text(str(args[2]))
    check_key(str(args[3]))
    if args[1] == 'e':
        print("".join(ceaser(list(args[2]), int(args[3]))))
    elif args[1] == 'd':
        print("".join(ceaser(list(args[2]), -int(args[3]))))


if __name__ == '__main__':
    main(["main.py", "e", "aBcd*123", "1"])
    main(["main.py", "d", "aBcd,123", "1"])
    main(["main.py", "e", "aBcd", "1"])
