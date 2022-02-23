import sys
import re

# set this to 1 for test mode
test = 1 # like macros define :)

letters_uppercase = "ABCDEFGHIJKLMOPQRSTUVWXYZ"
letters_lowercase = "abcdefghijklmnopqrstuvwxyz"
nums = "0123456789"


# Shift word on key and return result
def cesar(word: str, key: int) -> str:
    ret_list = list()
    
    for char in word:
        if str.isnumeric(char):
            index_of_char = nums.index(char)
            real_shift = (index_of_char + key) % 10
            char = nums[real_shift]
        elif str.islower(char):
            index_of_char = letters_lowercase.index(char)
            real_shift = (index_of_char + key) % 26
            char = letters_lowercase[real_shift]
        else:  # str.isupper(char)
            index_of_char = letters_uppercase.index(char)
            real_shift = (index_of_char + key) % 26
            char = letters_uppercase[real_shift]
        ret_list.append(char)
    return "".join(ret_list)


def main(args: list):
    args = " ".join(args[1:])
    # Так пойдет? :)
    # End of the string -------------------+
    # 1 or more digits ------------------+  \
    # 1 or more word characters ---+------\--\---word character is any english letter in any case or digit
    # Just space ----------------+--\---+  \  \
    # Charactar 'd' or 'e' --- +  \  \   \  \  \
    # Start of the string -+    \  \  \   \  \  \
    #                       \    \  \  \   \  \  \
    regex_res = re.search(r"\A([d|e]) (\w+) (\d+)\Z", args)
    # и вообще, как говорим МЫ, фанаты grep-а: "regex сила, ctrl+f могила"

    if regex_res is None:
        print("Invalid arguments!", file=sys.stderr)
        if test:
            return 1 # чтобы тесты не вылетели
        else:
            sys.exit(-1)

    crypt = regex_res.group(1)  # d or e
    word = regex_res.group(2)
    key = int(regex_res.group(3))

    if crypt == "e":
        print(cesar(word, key))
    else:
        print(cesar(word, -1 * key))


if __name__ == '__main__':
    if test: # прошлый вариант по-моему все-таки был лучше)
        main(["main.py","e", "Cesar123", "5"])
        main(["main.py","d", "Hjxfw678", "5"])
        main(["main.py","e", "ABCDefg155", "666"])
        main(["main.py","x", "Afdsfs1", "532"])
        main(["main.py","e", "AbcDef123!@$#!&$", "54"])
        main(["main.py","e", "ABCDef123", "54!@#"])
    else:
        main(sys.argv)
