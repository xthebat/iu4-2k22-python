import sys
import string


def main(args: list):
    if len(args) == 4:
        print(caesar(args[1], args[2], int(args[3])))
    else:
        print("Invalid parameters!")


def caesar(type: str, origin_string: str, shift: int) -> str:
    if type == 'd':
        shift = shift
    elif type == 'e':
        shift = -shift
    else:
        raise ValueError(
            "'type' can only take the values 'e' for encrypt or 'd' for decrypt")
    DICTIONARY = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([DICTIONARY[((DICTIONARY.index(char) + shift) % len(DICTIONARY))] if char in DICTIONARY else char for char in origin_string])


if __name__ == "__main__":
    main(sys.argv)
