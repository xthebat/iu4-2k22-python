import sys

codes = [list(range(48, 58)), list(range(65, 91)), list(range(97, 123))]


def arg_check(args: list) -> None:
    # Local constants
    op_type = set("de")
    cyrillic = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    # Check validity of an operation type
    if args[0] not in op_type:
        sys.exit("Choose either encrypt or decrypt")
    # Check that several languages are not presented in a string, i.e. russian language
    if cyrillic.isdisjoint(set(args[1].lower())) is False:
        sys.exit("Remember, no russian")
    # Check validity of a key
    if args[2].isdigit() is False:
        sys.exit("Key must be an integer")


def cipher(given_text: list, shift: int) -> str:
    answer = []
    digit_capacity = len(codes[0])
    english_capacity = len(codes[1])
    for sym in given_text:
        ascii_code = ord(sym)
        # Decrypt/encrypt if symbol is in [[0-9], [A-Z], [a-z]]
        if any(ascii_code in sub_codes for sub_codes in codes):
            # 0-9 cycle
            if ascii_code in codes[0]:
                new_sym = (ascii_code + shift -
                           codes[0][0]) % digit_capacity + codes[0][0]
            # A-Z cycle
            elif ascii_code in codes[1]:
                new_sym = (ascii_code + shift -
                           codes[1][0]) % english_capacity + codes[1][0]
            # a-z cycle
            elif ascii_code in codes[2]:
                new_sym = (ascii_code + shift -
                           codes[2][0]) % english_capacity + codes[2][0]
        # Leave spaces, special characters, etc. as they are
        else:
            new_sym = ascii_code
        answer.append(chr(new_sym))
    return "".join(answer)


def main(args: list) -> None:
    # Check for validity of the arguments
    arg_check(args)

    key = int(args[2])
    # Decrypt
    if args[0] == "d":
        print(cipher(args[1], -key))
    # Encrypt
    elif args[0] == "e":
        print(cipher(args[1], key))


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
