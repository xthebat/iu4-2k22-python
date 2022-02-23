import sys


def main(args: list) -> None:

    d_e = args[0]                       # decode/encode
    string_to_work = args[1]
    length = len(string_to_work)        # length of string_to_work
    key = args[2]                       # count for decode/encode
    transformed_string = [transformed_string*1 for transformed_string in string_to_work]
    print(transformed_string)

    if d_e == "e":                      # if you want to encode string, do following
        i = 0
        while i < length:               # we work with every symbol of string
            new_position = i
            i_1 = 0
            while i_1 < key:             # we count new position every symbol of string
                new_position += 1
                if new_position == length:
                    new_position = 0
                i_1 += 1
            transformed_string[new_position] = string_to_work[i]
            i += 1
    elif d_e == "d":                    # if you want to decode string, do following
        i = 0
        while i < length:               # we work with every symbol of string
            old_position = i+1
            i_1 = 0
            while i_1 < key:            # we count new position every symbol of string
                old_position -= 1
                print(old_position)
                if old_position == 0:
                    old_position = length
                i_1 += 1
            transformed_string[old_position-1] = string_to_work[i]
            i += 1

    print("".join(transformed_string))


if __name__ == '__main__':
    main(sys.argv)