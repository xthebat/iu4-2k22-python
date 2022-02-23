import sys


def cesar(d_e: int, string: str, key: int):
    result = ""
    if d_e == 0:  # encode:
        for letter in range(len(string)):
            if string[letter].isupper():
                result += chr((ord(string[letter]) + key - 65) % 26 + 65)
            elif string[letter].islower():
                result += chr((ord(string[letter]) + key - 97) % 26 + 97)
            elif string[letter].isnumeric():
                result += chr((ord(string[letter]) + key - 48) % 10 + 48)
            else:
                print("Improper value for the letter to encode")
                sys.exit(-1)
        return result
    elif d_e == 1:  # decode:
        for letter in range(len(string)):
            if string[letter].isupper():
                result += chr((ord(string[letter]) - key - 65) % 26 + 65)
            elif string[letter].islower():
                result += chr((ord(string[letter]) - key - 97) % 26 + 97)
            elif string[letter].isnumeric():
                result += chr((ord(string[letter]) - key - 48) % 10 + 48)
            else:
                print("Improper value for the letter to decode")
                sys.exit(-1)
        return result
    else:
        print("Improper value for the encode/decode function")
        sys.exit(-1)


def main(args):
    cont = 1
    while cont == 1:
        string = input("Enter the string:\n")
        key = int(input("Enter the key:\n"))
        e_d = int(input("Enter 0 to encode,\n\t  1 to decode the string:\n"))
        print(cesar(e_d, string, key), "\n")
        cont = int(input("Continue?\n1 - yes\n"))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
