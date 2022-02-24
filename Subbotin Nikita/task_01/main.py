import sys


def en_text_caesar(text: str, shift: int) -> str:
    alph = '0123456789ABCDEFGHIJKMLNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    new_text = ''

    for i in text:
        if i in alph:
            if ord('0') <= ord(i) <= ord('9') and shift > (ord('9')-ord(i)):
                new_text += chr(ord(i) + shift + 7)
            elif ord('A') <= ord(i) <= ord('Z') and shift > (ord('Z')-ord(i)):
                new_text += chr(ord(i) + shift + 6)
            elif ord('a') <= ord(i) <= ord('z') and shift > (ord('z')-ord(i)):
                new_text += chr(ord(i) + shift - 75)
            else:
                new_text += chr(ord(i) + shift)
        else:
            new_text += i
    return new_text


def de_text_caesar(text: str, shift: int) -> str:
    alph = '0123456789ABCDEFGHIJKMLNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    new_text = ''

    for i in text:
        if i in alph:
            if ord('0') <= ord(i) <= ord('9') and shift > (ord(i) - ord('0')):
                new_text += chr(ord(i) - shift + 75)
            elif ord('A') <= ord(i) <= ord('Z') and shift > (ord(i) - ord('A')):
                new_text += chr(ord(i) - shift - 7)
            elif ord('a') <= ord(i) <= ord('z') and shift > (ord(i) - ord('a')):
                new_text += chr(ord(i) - shift - 6)
            else:
                new_text += chr(ord(i) - shift)
        else:
            new_text += i
    return new_text


def main(args):
    c = 1
    while c == 1:

        d = 1
        while d == 1:
            dir = input("Enter direction: <d/e>:\n")
            if dir != 'd' and dir != 'e':
                print("Wrong direction!\n")
            else:
                d = 0

        string = input("Enter string (0-9A-Za-z):\n")

        while d == 0:
            key = int(input("Enter key (0-10):\n"))
            if key > 10 or key < 1:
                print("Wrong key!\n")
            else:
                d = 1

        if dir == 'd':
            print(de_text_caesar(string, key))
        elif dir == 'e':
            print(en_text_caesar(string, key))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)

