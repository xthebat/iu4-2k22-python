import sys


def caesar(type: str, string: str, shift: int) -> str:
    if type == 'd':
        shift = 26 - shift
    elif type != 'e':
        raise ValueError(
            "'type' can only take the values 'e' for encrypt or 'd' for decrypt")
    shift %= 27
    shifted_string_list = []
    for char in string:
        new_char = char
        if 'A' <= char <= 'Z':
            new_char = chr((ord(char) + shift - 65) % 26 + 65)
        elif 'a' <= char <= 'z':
            new_char = chr((ord(char) + shift - 97) % 26 + 97)
        shifted_string_list.append(new_char)
    return "".join(shifted_string_list)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 4:
        print(caesar(args[1], args[2], int(args[3])))
