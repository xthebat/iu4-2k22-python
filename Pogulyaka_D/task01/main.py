import sys
import string


digits = '1234567890'


def caesar_cipher(str_to_work: str, key: int) -> str:
    abc = string.ascii_lowercase
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
    return "".join(str_res)


def main(args: list):
    if args[1] == 'e':
        print(caesar_cipher(args[2], int(args[3])))
    if args[1] == 'd':
        print(caesar_cipher(args[2], -int(args[3])))


if __name__ == '__main__':
    main(sys.argv)
    # main(['main.py', 'd', "nkvbj1 2145 jgfdkk    TyUo1 && asdjq. uud, uas", '12345'])
    # main(['main.py', 'e', "BASDioo1234 ka, isd", '10'])
    # main(['main.py', 'd', "abcd1234 defg567", '1'])
