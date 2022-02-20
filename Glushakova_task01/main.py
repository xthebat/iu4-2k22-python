import sys


def main(args):
    shifr = args[1]
    string = list(args[2])
    int_k = int(args[3])

    if shifr == 'e':
        print(string)
        int_i = 0
        for symbol in string:
            if (int_i + int_k) != len(string):
                a = symbol
                string[int_i] = string[int_i + int_k]
                string[int_i + int_k] = a
                int_i += 1
        print(string)

    if shifr == 'd':
        print(string)
        int_i = len(string) - 1
        while int_i >= int_k:
            a = string[int_i - int_k]
            string[int_i - int_k] = string[int_i]
            string[int_i] = a
            int_i -= 1
        print(string)


if __name__ == '__main__':
    main(sys.argv)
