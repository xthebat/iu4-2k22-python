
import sys


DICTIONARY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "


def caesar_cipher(list_work: list, int_key: int) -> str:
    int_i = 0
    for item in list_work:
        list_work[int_i] = DICTIONARY[(DICTIONARY.find(item) + int_key) % len(DICTIONARY)]
        int_i += 1
    return "".join(list_work)


def main(args: list):
    int_key = int(args[3])
    if args[1] == 'd':
        int_key *= -1
    elif args[1] != 'e':
        print("Invalid param1")
        sys.exit(-1)
    print(caesar_cipher(list(args[2]), int_key))
    sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)

