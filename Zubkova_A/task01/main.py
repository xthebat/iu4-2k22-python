import sys
alfavit = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main(args):
    s = int(args[1])  # шаг
    sms = args[2].upper()  # слово
    new = ''  # новое слово
    for i in sms:
        mesto = alfavit.find(i)    # позиция
        new_mesto = mesto + s    # Сдвиг
        if i in alfavit:
            new += alfavit[new_mesto]  # зашифрованное
        else:
            new += i
        print(new)


if __name__ == '__main__':
    main(sys.argv)