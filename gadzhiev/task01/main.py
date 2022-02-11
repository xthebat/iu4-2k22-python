import sys


def main(args: list):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    dec_enc = str(args[1])
    if (dec_enc != "d") & (dec_enc != "e"):
        print("invalid parameter for encoding")
        sys.exit(-1)
    input_string = str(args[2])
    input_str_list = list(args[2])
    key = int(args[3])
    if dec_enc == "d":      # encrypt or decrypt
        key = -key
    output_string = encrypt_decrypt(input_str_list, alphabet, key)
    print("input string: ", input_string)
    print("key: ", abs(key))
    print("output string: ", output_string)


def encrypt_decrypt(input_str_list: list, alphabet: str, key: int) -> str:
    i = 0
    for item in input_str_list:
        x = alphabet.find(item)
        print(x, " ", alphabet[x])
        if (x >= 0) & (x <= 25):         # uppercase
            x = (x + key) % 26
        elif (x >= 26) & (x <= 51):      # lowercase
            x = (x + key) % 52 + 26
            if x > 51:
                x = x - 26
        elif (x >= 52) & (x <= 61):      # number
            x = (x + key) % 62 + 52
            if x > 61:
                x = x - 52
        if x == -1:                     # not in the alphabet
            input_str_list[input_str_list.index(item)] = item
        else:                           # is in the alphabet
            input_str_list[i] = alphabet[x]
        i += 1
        print(x, " ", alphabet[x])
    output_string = "".join(input_str_list)
    return output_string


if __name__ == '__main__':
    main(sys.argv)