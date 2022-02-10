import sys
import re
'''
    Поздно увидел, что в дискорде есть прямое указание, какие аргументы использовать
    Если надо сделать именно как вы написали, то сделаю, тут не долго
    Заодно количество строк уменьшиться :)
'''


# Just print help
def print_help():
    print(" --------       HELP       -------- ")
    print("Use '-encrypt <word>' to encrypt your word")
    print("Use '-decrypt <word>' to decrypt your word")
    print("Use '-shift <shift>'  to set shift of encrypt/decrypt")
    print("Use '-help'           to print this message\n")
    print("You can use args in any order you like")
    print("But you can't use '-encrypt' and '-decrypt' args at the same time\n")
    print(" --------      Example     -------- ")
    print("main.py -encrypt Cesar -shift 3")
    print("Output: Fhvdu")
    print("main.py -decrypt Fhvdu -shift 3")
    print("Output: Cesar")


# Return value of argument from arguments list
# Return None if argument not found
def get_arg(args: list, arg_to_find: str):
    args_len = len(args)

    for i in range(args_len):
        arg = args[i]
        if arg == arg_to_find and (i + 1) < args_len:
            return args[i+1]
        elif arg == arg_to_find and arg == "-help":
            return True

    return None


# Print encrypted/decrypted word with shift according flag 'encrypt'
def print_crypted_word(word: str, shift: int, encrypt: bool):
    letters_uppercase = list("ABCDEFGHIJKLMOPQRSTUVWXYZ")
    letters_lowercase = list("abcdefghijklmnopqrstuvwxyz")
    nums = list("0123456789")

    if encrypt:
        for char in word:
            if str.isnumeric(char):
                index_of_char = nums.index(char)
                real_shift = (index_of_char + shift) % 10
                char = nums[real_shift]
            elif str.islower(char):
                index_of_char = letters_lowercase.index(char)
                real_shift = (index_of_char + shift) % 26
                char = letters_lowercase[real_shift]
            else:  # str.isupper(char)
                index_of_char = letters_uppercase.index(char)
                real_shift = (index_of_char + shift) % 26
                char = letters_uppercase[real_shift]
            print(char, end="")
    else:
        for char in word:
            if str.isnumeric(char):
                index_of_char = nums.index(char)
                real_shift = (index_of_char - shift) % 10
                char = nums[real_shift]
            elif str.islower(char):
                index_of_char = letters_lowercase.index(char)
                real_shift = (index_of_char - shift) % 26
                char = letters_lowercase[real_shift]
            else:
                index_of_char = letters_uppercase.index(char)
                real_shift = (index_of_char - shift) % 26
                char = letters_uppercase[real_shift]
            print(char, end="")
    print()


def main(args: list):
    word_to_encrypt = get_arg(args, "-encrypt")
    word_to_decrypt = get_arg(args, "-decrypt")
    shift = get_arg(args, "-shift")
    help_arg = get_arg(args, "-help")
    encrypt = word_to_encrypt is not None
    decrypt = word_to_decrypt is not None

    if help_arg:
        print_help()

    # Защита от дурака
    if encrypt and decrypt:
        print("Using -encrypt and -decrypt args together is invalid", file=sys.stderr)
        return 1

    if shift is None or not str.isnumeric(shift) or (not encrypt and not decrypt):
        print("Invalid arguments to encrypt/decrypt!", file=sys.stderr)
        if help_arg is None:
            print("Use -help to get information about arguments", file=sys.stderr)
        return 1

    # А это в алфавит укладывается?
    if encrypt:
        regex = re.search(r"\W+", word_to_encrypt)
    else:
        regex = re.search(r"\W+", word_to_decrypt)

    if regex is not None:
        print("\"", regex.group(0), "\" is not a word!", sep='', file=sys.stderr)
        return 1

    shift = int(shift)

    # непосредственно шифрование/дешифрование
    if encrypt:
        print_crypted_word(word_to_encrypt, shift, True)
    else:
        print_crypted_word(word_to_decrypt, shift, False)


if __name__ == '__main__':
    main(sys.argv)
