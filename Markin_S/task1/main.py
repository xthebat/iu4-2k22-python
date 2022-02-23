import sys
import string


def main(args: list):
    if len(args) == 4:
        cipher(args[1], args[2], int(args[3]))
    else:
        print("Arguments not provided")
        print("U need to use 3 argument which is: <d/e> <string-to-work> <key>")


def cipher(cipher_method: str, string_to_work: str, key: int):
    if cipher_method == 'e':
        key = key
    elif cipher_method == 'd':
        key = -key
    else:
        print(f"<{cipher_method}> is not true argument to use")
        sys.exit(-1)
    res = ""
    for ch in string_to_work:
        if ch.isdigit():
            alphabet = string.digits
        elif ch.islower():
            alphabet = string.ascii_lowercase
        else:
            alphabet = string.ascii_uppercase
        index = alphabet.find(ch)
        res += alphabet[(index + key) % len(alphabet)]
    print(res)


if __name__ == '__main__':
    main(sys.argv)
