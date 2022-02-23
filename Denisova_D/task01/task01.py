import sys


def task01(args: list):
    if len(args) != 4:
        print("Invalid args: more or less arguments")
    sys.exit(-1)

    if args[1] == "d":
        mode = -1
    elif args[1] == "e":
        mode = 1
    else:
        print("Invalid argument: <d/e>")
        sys.exit(-1)

    t = str(args[2])
    "".join(t)
    key = str(args[3])
    "".join(key)
    key = int(key)

    if args[1] == 'd':
        decryption(t, key)
    elif args[1] == 'e':
        encryption(t, key)


def encryption(string, shag):
    result = ''
    for i in range(len(string)):
        char = string[i]
        if char.isupper():
            result += chr((ord(char) + shag - 1 - 64) % 26 + 65)
        if char.islower():
            result += chr((ord(char) + shag - 1 - 96) % 26 + 97)
        if char.isdigit():
            result += chr((ord(char) + shag - 1 - 47) % 10 + 48)
    print(result)


def decryption(string, shag):
    result = ''
    for i in range(len(string)):
        char = string[i]
        if char.isupper():
            result += chr((ord(char) - shag + 1 + 65) % 26 + 64)
        if char.islower():
            result += chr((ord(char) - shag + 1 + 85) % 26 + 96)
        if char.isdigit():
            result += chr((ord(char) - shag + 1 + 41) % 10 + 48)
    print(result)


if __name__ == '__task01__':
    task01(sys.argv)
