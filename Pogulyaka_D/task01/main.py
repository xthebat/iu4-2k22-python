import sys
import string


def caesar_cipher(str_to_work, key):
    abc = string.ascii_lowercase
    digits = '1234567890'
    str_res = []
    for item in str_to_work:
        if item.isdigit():
            index = (digits.index(item) + key) % len(digits)
            str_res.append(digits[index])
        elif item.islower():
            index = (abc.index(item) + key) % len(abc)
            str_res.append(abc[index])
        elif item.isupper():
            index = (abc.upper().index(item) + key) % len(abc)
            str_res.append(abc[index].upper())
        else:
            str_res.append(item)
    print("".join(str_res))


def main(args: list):
    if args[1] == 'e':
        caesar_cipher(args[2], int(args[3]))
    if args[1] == 'd':
        caesar_cipher(args[2], -int(args[3]))


if __name__ == '__main__':
    main(sys.argv)
    #main(['main.py', 'd', "nkvbj1 2145 jgfdkk    TyUo1 && asdjq. uud, uas", '12345'])
    #main(['main.py', 'e', "BASDioo1234 ka, isd", '10'])
    #main(['main.py', 'd', "abcd1234 defg567", '1'])
