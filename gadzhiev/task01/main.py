import sys

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def main(args: list):
    dec_enc = str(args[1])
    if dec_enc != "d" and dec_enc != "e":
        print("invalid parameter for encoding")
        sys.exit(-1)
    input_string = str(args[2])
    input_str_list = list(args[2])
    key = int(args[3])
    if dec_enc == "d":  # encrypt or decrypt
        key = -key
    output_string = encrypt_decrypt(input_str_list, key)
    print("input string: ", input_string)
    print("key: ", abs(key))
    print("output string: ", output_string)


def encrypt_decrypt(input_str_list: list, key: int) -> str:
    i = 0
    for item in input_str_list:
        x = (alphabet.index(item) + key) % len(alphabet)
        input_str_list[i] = alphabet[x]
        i += 1
    output_string = "".join(input_str_list)
    return output_string


if __name__ == '__main__':
    main(sys.argv)

