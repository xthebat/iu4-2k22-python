import sys


def Enc_or_dec(cod: str, str_original: list, k: int):
    str_code = str_original
    int_i = 0
    if cod == 'e':
        for symbol in str_original:
            ascii_symbol = ord(symbol)
            if '1' <= symbol <= '9':
                if (ascii_symbol + k) > 57:
                    str_code[int_i] = chr(ascii_symbol - int((ascii_symbol + k) % 10))
                else:
                    str_code[int_i] = chr(ascii_symbol + k)
            elif 65 <= ascii_symbol <= 90:
                if (ascii_symbol + k) > 90:
                    str_code[int_i] = chr(ascii_symbol - int((ascii_symbol + k) % 26))
                else:
                    str_code[int_i] = chr(ascii_symbol + k)
            else:
                if (ascii_symbol + k) > 122:
                    str_code[int_i] = chr(ascii_symbol - int((ascii_symbol + k) % 26))
                else:
                    str_code[int_i] = chr(ascii_symbol + k)
            int_i += 1
    if cod == 'd':
        for symbol in str_original:
            ascii_symbol = ord(symbol)
            if '1' <= symbol <= '9':
                if (ascii_symbol - k) < 48:
                    str_code[int_i] = chr(ascii_symbol - k + 10)
                else:
                    str_code[int_i] = chr(ascii_symbol - k)
            elif 65 <= ascii_symbol <= 90:
                if (ascii_symbol - k) < 65:
                    str_code[int_i] = chr(ascii_symbol - k + 26)
                else:
                    str_code[int_i] = chr(ascii_symbol - k)
            else:
                if (ascii_symbol - k) < 97:
                    str_code[int_i] = chr(ascii_symbol - k + 26)
                else:
                    str_code[int_i] = chr(ascii_symbol - k)
            int_i += 1
    print(str_code)

def main(args):
    cod = args[1]
    string = list(args[2])
    int_k = int(args[3])

    Enc_or_dec(cod, string, int_k)


if __name__ == '__main__':
    main(sys.argv)
