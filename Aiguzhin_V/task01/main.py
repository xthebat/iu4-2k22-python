import sys

op_type = set("de")
cyrillic = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
english_capacity = 26
digit_capacity = 10
codes = [list(range(48, 58)), list(range(65, 91)), list(range(97, 123))]


def arg_check(args: list) -> None:
    # Check validity of an operation type
    if args[0] not in op_type:
        sys.exit("Choose either encrypt or decrypt")
    # Check that several languages are not presented in a string, i.e. russian language
    if cyrillic.isdisjoint(set(args[1].lower())) is False:
        sys.exit("Remember, no russian")
    # Check validity of a key
    if args[2].isdigit() is False:
        sys.exit("Key must be integer")


def decrypt(enc_text: list, key: str) -> str:
    decr_text = []
    new_sym = None
    for x in enc_text:
        ascii_code = ord(x)
        # Decrypt only if symbol is in [[0-9], [A-Z], [a-z]]
        if any(ascii_code in sub_codes for sub_codes in codes):
            # 0-9 cycle
            if ascii_code in codes[0]:
                new_sym = (ascii_code - int(key) - codes[0][0]) % digit_capacity + codes[0][0]
            # A-Z cycle
            elif ascii_code in codes[1]:
                new_sym = (ascii_code - int(key) - codes[1][0]) % english_capacity + codes[1][0]
            # a-z cycle
            elif ascii_code in codes[2]:
                new_sym = (ascii_code - int(key) - codes[2][0]) % english_capacity + codes[2][0]
        else:
            new_sym = ascii_code
        # Leave spaces, special characters etc. as they are
        decr_text.append(chr(new_sym))
    return "".join(decr_text)


def encrypt(dec_text: list, key: str) -> str:
    enc_text = []
    new_sym = None
    for x in dec_text:
        ascii_code = ord(x)
        # Encrypt only if symbol is in [[0-9], [A-Z], [a-z]]
        if any(ascii_code in sub_codes for sub_codes in codes):
            # 0-9 cycle
            if ascii_code in codes[0]:
                new_sym = (ascii_code + int(key) - codes[0][0]) % digit_capacity + codes[0][0]
            # A-Z cycle
            elif ascii_code in codes[1]:
                new_sym = (ascii_code + int(key) - codes[1][0]) % english_capacity + codes[1][0]
            # a-z cycle
            elif ascii_code in codes[2]:
                new_sym = (ascii_code + int(key) - codes[2][0]) % english_capacity + codes[2][0]
        # Leave spaces, special characters etc. as they are
        else:
            new_sym = ascii_code
        enc_text.append(chr(new_sym))
    return "".join(enc_text)


def main(args: list) -> None:
    # Check for validity of the arguments
    arg_check(args)
    # Decrypt
    if args[0] == "d":
        print(decrypt(args[1], args[2]))
    # Encrypt
    elif args[0] == "e":
        print(encrypt(args[1], args[2]))


if __name__ == '__main__':
    # Argument func check
    #main(["z", "wasd", "3"])
    #main(["d", "цadнwd", "2"])
    #main(["e", "kek", "i"])

    # Caesar cipher
    main(["e", "make love not war", "2"])
    main(["d", "plon", "3"])
    main(["e", "anarchy13", "10"])
    main(["d", "%qb% !lbh! [yvxr] #uhegvat# @bgure@ ?crbcyr?", "13"])
