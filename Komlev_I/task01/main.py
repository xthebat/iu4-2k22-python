import sys
import string
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGIT = string.digits
PUNCT = string.punctuation
ALL_TEXT = string.ascii_letters + DIGIT + PUNCT


def encryption(alphabet: str, char: str, key: int):
    new_char = alphabet[(alphabet.index(char) + key) % len(alphabet)]
    return new_char


def check_text(text: str):
    for char in text:
        if char not in ALL_TEXT+" ":
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


def ceaser(text: str, key: int) -> str:
    result = []
    for char in text:
        if char.islower():
            new_char = encryption(LOWER, char, key)
            result.append(new_char)
        elif char.isupper():
            new_char = encryption(UPPER, char, key)
            result.append(new_char)
        elif char.isdigit():
            new_char = encryption(DIGIT, char, key)
            result.append(new_char)
        else:
            result.append(char)
    return "".join(result)


def main(args: list):
    check_argument(len(args))
    check_command(str(args[1]))
    check_text(str(args[2]))
    check_key(str(args[3]))
    if args[1] == 'e':
        print(ceaser(str(args[2]), int(args[3])))
    elif args[1] == 'd':
        print(ceaser(str(args[2]), -int(args[3])))


if __name__ == '__main__':
    main(["main.py", "e", "aBcd *123", "1"])
    main(["main.py", "d", "aBcd,123", "1"])
    main(["main.py", "e", "aBcd", "1"])
    main(["main.py", "e", "aBcd", "1", "adsf"])
