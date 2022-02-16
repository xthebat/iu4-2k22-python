import sys
import string


def main(args: list):
    if len(args) != 3:
        print("Invalid parameters")
        sys.exit(-1)
    action = args[0]
    if action != "d" and action != "e":
        print("Invalid action")
        sys.exit(-1)
    text = list(args[1])
    for i in range(len(text)):
        if text[i] not in string.ascii_letters+string.digits+string.punctuation:
            print("Invalid symbol in the text")
            sys.exit(-1)
    key = args[2]
    for i in range(len(key)):
        if key[i] in string.ascii_letters+string.punctuation and (key[i] != "-"):
            print("Invalid key")
            sys.exit(-1)
    key = int(args[2])
    if action == "e":
        for i in range(len(text)):
            if text[i] in string.ascii_lowercase:
                text[i] = string.ascii_lowercase[(string.ascii_lowercase.find(text[i])+key) % 26]
            elif text[i] in string.ascii_uppercase:
                text[i] = string.ascii_uppercase[(string.ascii_uppercase.find(text[i])+key) % 26]
            elif text[i] in string.digits:
                text[i] = string.digits[(string.digits.find(text[i])+key) % 10]
            elif text[i] in string.punctuation:
                text[i] = text[i]
        print("Encrypted text:", "".join(text))
    elif action == "d":
        for i in range(len(text)):
            if text[i] in string.ascii_lowercase:
                text[i] = string.ascii_lowercase[(string.ascii_lowercase.find(text[i])-key) % 26]
            elif text[i] in string.ascii_uppercase:
                text[i] = string.ascii_uppercase[(string.ascii_uppercase.find(text[i])-key) % 26]
            elif text[i] in string.digits:
                text[i] = string.digits[(string.digits.find(text[i])-key) % 10]
            elif text[i] in string.punctuation:
                text[i] = text[i]
        print("Dencrypted text:", "".join(text))


if __name__ == '__main__':
    main(["e", "aBcd*123", "1"])
    main(["d", "aBcd,123", "1"])
    main(["e", "aBcdИ", "1"])