import sys
def main(args:list):
    result = ""
    string_to_encrypt = "a b c d e f g h i j k l m n o p q r s t u v w x y z " \
                        "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z " \
                        "0 1 2 3 4 5 6 7 8 9"
    string_to_encrypt_slitted = string_to_encrypt.split(' ')
    if args[1].lower() == 'd':
        for alphabet_index in args[3]:
            try:
                current_index = string_to_encrypt_slitted.index(alphabet_index)
                if alphabet_index.isupper() == True:
                    if int(current_index) + int(args[2]) > 52:
                        modified_index = int(current_index) + int(args[2]) - 26
                        result += string_to_encrypt_slitted[modified_index]
                    else:
                        modified_index = current_index + int(args[2])
                        result += string_to_encrypt_slitted[modified_index]
                elif alphabet_index.islower() == True:
                    if int(current_index) + int(args[2]) > 26:
                        modified_index = int(current_index) + int(args[2]) - 26
                        result += string_to_encrypt_slitted[modified_index]
                    else:
                        modified_index = current_index + int(args[2])
                        result += string_to_encrypt_slitted[modified_index]
                elif alphabet_index.isdigit() == True:
                    if int(current_index) + int(args[2]) > 62:
                        modified_index = int(current_index) + int(args[2]) - 10
                        result += string_to_encrypt_slitted[modified_index]
                    else:
                        modified_index = int(current_index) + int(args[2])
                        result += string_to_encrypt_slitted[modified_index]
            except ValueError:
                result += alphabet_index
        print(result)

    elif args[1].lower() == 'e':
        for alphabet_index in args[3]:
            try:
                current_index = string_to_encrypt_slitted.index(alphabet_index)
                if alphabet_index.isupper() == True:
                    if int(current_index) - int(args[2]) < 26:
                        modified_index = int(current_index) - int(args[2]) + 26
                        result += string_to_encrypt_slitted[modified_index]
                    else:
                        modified_index = current_index - int(args[2])
                        result += string_to_encrypt_slitted[modified_index]
                elif alphabet_index.islower() == True:
                    if int(current_index) - int(args[2]) <= 0:
                        modified_index = int(current_index) - int(args[2]) + 26
                        result += string_to_encrypt_slitted[modified_index]
                    else:
                        modified_index = current_index - int(args[2])
                        result += string_to_encrypt_slitted[modified_index]
                elif alphabet_index.isdigit() == True:
                    if int(current_index) - int(args[2]) < 52:
                        modified_index = int(current_index) - int(args[2]) + 10
                        result += string_to_encrypt_slitted[modified_index]
                    else:
                        modified_index = int(current_index) - int(args[2])
                        result += string_to_encrypt_slitted[modified_index]
            except ValueError:
                result += alphabet_index
        print(result)
    else:
        print("Invalid decrypt/encrypt parameter - press e or d")

if __name__ == '__main__':
    main(sys.argv)
