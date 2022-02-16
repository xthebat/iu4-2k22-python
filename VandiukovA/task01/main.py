import sys


def main(args: list):
    result = ""
    string_to_encrypt = "a b c d e f g h i j k l m n o p q r s t u v w x y z " \
                        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z " \
                        "0 1 2 3 4 5 6 7 8 9"
    string_to_encrypt_splitted = string_to_encrypt.split(' ')
    if args[1].lower() == 'e':
        for alphabet_index in args[2]:
            try:
                current_index = string_to_encrypt_splitted.index(
                    alphabet_index)
                if alphabet_index.isupper():
                    if int(current_index) + int(args[3]) > 52:
                        modified_index = int(current_index) + int(args[3]) - 26
                        result += string_to_encrypt_splitted[modified_index]
                    else:
                        modified_index = current_index + int(args[3])
                        result += string_to_encrypt_splitted[modified_index]
                elif alphabet_index.islower():
                    if int(current_index) + int(args[3]) > 26:
                        modified_index = int(current_index) + int(args[3]) - 26
                        result += string_to_encrypt_splitted[modified_index]
                    else:
                        modified_index = current_index + int(args[3])
                        result += string_to_encrypt_splitted[modified_index]
                elif alphabet_index.isdigit():
                    if int(current_index) + int(args[3]) > 61:
                        modified_index = int(current_index) + int(args[3]) - 10
                        result += string_to_encrypt_splitted[modified_index]
                    else:
                        modified_index = int(current_index) + int(args[3])
                        result += string_to_encrypt_splitted[modified_index]
            except ValueError:
                result += alphabet_index
        print(result)

    elif args[1].lower() == 'd':
        for alphabet_index in args[2]:
            try:
                current_index = string_to_encrypt_splitted.index(
                    alphabet_index)
                if alphabet_index.isupper():
                    if int(current_index) - int(args[3]) < 26:
                        modified_index = int(current_index) - int(args[3]) + 26
                        result += string_to_encrypt_splitted[modified_index]
                    else:
                        modified_index = current_index - int(args[3])
                        result += string_to_encrypt_splitted[modified_index]
                elif alphabet_index.islower():
                    if int(current_index) - int(args[3]) < 0:
                        modified_index = int(current_index) - int(args[3]) + 26
                        result += string_to_encrypt_splitted[modified_index]
                    else:
                        modified_index = current_index - int(args[3])
                        result += string_to_encrypt_splitted[modified_index]
                elif alphabet_index.isdigit():
                    if int(current_index) - int(args[3]) < 52:
                        modified_index = int(current_index) - int(args[3]) + 10
                        result += string_to_encrypt_splitted[modified_index]
                    else:
                        modified_index = int(current_index) - int(args[3])
                        result += string_to_encrypt_splitted[modified_index]
            except ValueError:
                result += alphabet_index
        print(result)
    else:
        print("Invalid decrypt/encrypt parameter - press e or d")
    return result


if __name__ == '__main__':
    main(sys.argv)
