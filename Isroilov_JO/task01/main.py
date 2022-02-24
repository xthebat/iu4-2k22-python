import sys


def main(args: list):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    res = ''
    s = args[1]
    mod = args[2]

    if args[0] == 'inc':
        for sym in s:
            if sym in alphabet:
                a = alphabet.find(sym)
                new_mod = (a + int(mod)) % len(alphabet)
                res += alphabet[new_mod]
    elif args[0] == 'dec':
        for sym in s:
            if sym in alphabet:
                a = alphabet.find(sym)
                new_mod = (a - int(mod)) % len(alphabet)
                res += alphabet[new_mod]

    print(res)


if __name__ == '__main__':
    main(sys.argv)
