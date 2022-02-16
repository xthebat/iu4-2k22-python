import sys
import string


def main(args: list):
    if len(args) != 4:
        print("Invalid args: more or less arguments")
        sys.exit(-1)

    if args[1] == "d":
        mode = -1
    elif args[1] == "e":
        mode = 1
    else:
        print("Invalid argument: <d/e>")
        sys.exit(-1)

    for x in range(len(args[3])):
        if args[3][x] in string.ascii_letters + string.punctuation and (args[3][x] != "-"):
            print("Invalid argument: <key>")
            sys.exit(-1)

    key = int(args[3])
    smbls = list(args[2])

    for x in range(len(args[2])):
        if smbls[x] in string.ascii_lowercase:
            shift = (string.ascii_lowercase.find(smbls[x]) + mode * key) % 26
            smbls[x] = string.ascii_lowercase[shift]
        elif smbls[x] in string.ascii_uppercase:
            shift = (string.ascii_uppercase.find(smbls[x]) + mode * key) % 26
            smbls[x] = string.ascii_uppercase[shift]
        elif smbls[x] in string.digits:
            shift = (string.digits.find(smbls[x]) + mode * key) % 10
            smbls[x] = string.digits[shift]

    print("".join(smbls))


if __name__ == '__main__':
    main(["./main.py", "e", "abcd", "1"])
    main(["./main.py", "d", "abcd", "1"])
    main(["./main.py", "e", "abcd", "-1"])
    main(["./main.py", "d", "abcd", "-1"])
