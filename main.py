import sys
num = '0123456789'
uc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lc = 'abcdefghijklmnopqrstuvwxyz'


def rewrite(dictionary: str, i: str, key: int, finish_str: list):
    a = (dictionary.index(i) + key) % len(dictionary)
    finish_str.append(dictionary[a])


def caesar(de: str, string_to_work: str, key: int) -> str:
    finish_str = []
    if de == 'd':
        key = -key
    elif de != 'e':
        print("Not expected value d/e:", de)
        sys.exit(-1)
    for i in string_to_work:
        if i in num:
            rewrite(num, i, key, finish_str)
        elif i in uc:
            rewrite(uc, i, key, finish_str)
        elif i in lc:
            rewrite(lc, i, key, finish_str)
        else:
            print("Invalid symbol:", i)
            sys.exit(-1)
    return "".join(finish_str)


def main(arg: list):
    if len(arg) != 4:
        print("Wrong number of values", len(arg))
        sys.exit(-1)
    print("Old value:", arg[2])
    print("New value:", caesar(arg[1], arg[2], int(arg[3])))
    print("dec value:", caesar(arg[1], caesar(arg[1], arg[2], int(arg[3])), -int(arg[3])))


if __name__ == '__main__':
    main(sys.argv)