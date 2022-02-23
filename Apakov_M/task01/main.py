import sys
import string


def main(args: list):
    if len(args) != 4:
        print('Error: only 4 parameters')
        sys.exit(-1)
    if not args[3].isnumeric():
        print('Error: shift must be positive numeric')
        sys.exit(-2)
    if args[1].lower() == 'e':
        print(caesar(args[2], int(args[3])))
    elif args[1].lower() == 'd':
        print(caesar(args[2], -int(args[3])))
    else:
        print('Error: only E or D')
        sys.exit(-3)


def caesar(string_to_work: str, shift: int) -> str:
    ALPHABET = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result = []
    for char in string_to_work:
        if char in ALPHABET:
            result.append(
                ALPHABET[(ALPHABET.find(char) + shift) % len(ALPHABET)])
        else:
            result.append(char)
    return "".join(result)


if __name__ == "__main__":
    # main(sys.argv)
    main(["", "e", "make love not war", "10"])
    main(["", "d", "wkuo vyFo xyD GkB", "10"])
