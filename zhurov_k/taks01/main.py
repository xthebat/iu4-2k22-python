import sys
import string


def cesar(direction, input_string, key_str):
    output_string = list(input_string)
    key = int(key_str)

    if direction == "d":
        key *= -1
    elif direction != "e":
        return None

    for x in range(len(output_string)):
        if output_string[x] in string.ascii_lowercase:
            output_string[x] = _cesar_shift(output_string[x], string.ascii_lowercase, key)
        elif output_string[x] in string.ascii_uppercase:
            output_string[x] = _cesar_shift(output_string[x], string.ascii_uppercase, key)
        elif output_string[x] in string.digits:
            output_string[x] = _cesar_shift(output_string[x], string.digits, key)

    return "".join(output_string)


def _cesar_shift(input_string, dictionary, key):
    shift = (dictionary.find(input_string) + key) % len(dictionary)
    return dictionary[shift]


def main(args: list):
    if args[1] == "testing":
        print("Test 1: encrypt/decrypt with lowercase, uppercase, numbers and punctuation (key = 1): ")
        print("\tEncrypt result: abc,DEF,!&^%#,123 -> ", cesar("e", "abc,DEF,!&^%#,123", 1))
        print("\tDecrypt result: bcd,EFG,!&^%#,234 -> ", cesar("d", "bcd,EFG,!&^%#,234", 1))

        print("Test 2: encrypt/decrypt with big key, to create loop in dictionary (key = 32): ")
        print("\tEncrypt result: abc,DEF,!&^%#,123 -> ", cesar("e", "abc,DEF,!&^%#,123", 32))
        print("\tDecrypt result: ghi,JKL,!&^%#,345 -> ", cesar("d", "ghi,JKL,!&^%#,345", 32))

        print("Test 3: encrypt/decrypt with negative key (key = -10): ")
        print("\tEncrypt result: abc,DEF,!&^%#,123 -> ", cesar("e", "abc,DEF,!&^%#,123", -16))
        print("\tDecrypt result: klm,NOP,!&^%#,567 -> ", cesar("d", "klm,NOP,!&^%#,567", -16))

        print("Test 4: encrypt/decrypt with big negative key, to create loop in dictionary (key = -32): ")
        print("\tEncrypt result: abc,DEF,!&^%#,123 -> ", cesar("e", "abc,DEF,!&^%#,123", -32))
        print("\tDecrypt result: uvw,XYZ,!&^%#,901 -> ", cesar("d", "uvw,XYZ,!&^%#,901", -32))

        print("Test 5: double encrypt/decrypt (key = 8 and -21): ")
        print("\tEncrypt result: abc,DEF,!&^%#,123",
              "--( 8 )->",
              cesar("e", "abc,DEF,!&^%#,123", 8),
              "--(-21)->z",
              cesar("e", cesar("e", "abc,DEF,!&^%#,123", 8), -21)
              )
        print("\tDecrypt result: nop,QRS,!&^%#,890",
              "--(-21)->",
              cesar("d", "nop,QRS,!&^%#,890", -21),
              "--( 8 )->",
              cesar("d", cesar("d", "nop,QRS,!&^%#,890", -21), 8)
              )

        return

    if len(args) != 4:
        print("Invalid args: more or less arguments")
        sys.exit(-1)

    if args[1] != "d" and args[1] != "e":
        print("Invalid argument: <d/e>")
        sys.exit(-1)

    for x in range(len(args[3])):
        if args[3][x] in string.ascii_letters + string.punctuation and (args[3][x] != "-"):
            print("Invalid argument: <key>")
            sys.exit(-1)

    print("Result ", args[2], "--(", args[3], ")->", cesar(args[1], args[2], args[3]))


if __name__ == '__main__':
    main(sys.argv)
