import sys


def main(args: list):
    if len(args) != 4:
        print("Invalid number of parameters")
        sys.exit(-1)
    if args[1] != "d" and args[1] != "e":
        print("Invalid command! Please specify 'd' or 'e'.")
        sys.exit(-1)
    if not args[2].isalnum():
        print("Invalid command. Please specify the numbers")
        sys.exit(-1)
        
    l = str(args[2])
    "".join(l)
    key = str(args[3])
    "".join(key)
    key = int(key)

    if args[1] == 'd':
        decryption(l, key)
    elif args[1] == 'e':
        encryption(l, key)

    stra = "ABC"
    stra1 = chr(ord('A'))
    print("".join([stra, stra1]))

def encryption(string, shift):
    result = ''
    for i in range(len(string)):
        char = string[i]
        if char.isupper():
            result = "".join([result, chr((ord(char) + shift - 1 - 64) % 26 + 65)])
        if char.islower():
            result = "".join([result, chr((ord(char) + shift - 1 - 96) % 26 + 97)])
        if char.isdigit():
            result = "".join([result, chr((ord(char) + shift - 1 - 47) % 10 + 48)])

    print(result)


def decryption(string, shift):
    result = ''
    for i in range(len(string)):
        char = string[i]
        if char.isupper():
            result = "".join([result, chr((ord(char) - shift + 1 + 65) % 26 + 64)])
        if char.islower():
            result = "".join([result, chr((ord(char) - shift + 1 + 85) % 26 + 96)])
        if char.isdigit():
            result = "".join([result, chr((ord(char) - shift + 1 + 41) % 10 + 48)])
    print(result)


if __name__ == '__main__':
    main(sys.argv)
