from caesar import *


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 "


def main(args: list):
    if len(args) != 4:
        error("Three arguments are expected")
    input_data = CommandStringData(args[1:])

    mode = input_data.mode
    string_to_work = input_data.string_to_work
    key = input_data.key

    encryption = Caesar(key)
    result = encryption.start(string_to_work, ALPHABET, mode)
    print(f"Result: {result}")


if __name__ == '__main__':
    main(sys.argv)
