import sys

lib_small_en = 'abcdefghijklmnopqrstuvwxyz'
lib_big_en = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lib_small_ru = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
lib_big_ru = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

res = ''
def main(args):
    flag_code, string_value, key_value = '', '', ''
    if len(args) == 4:
        flag_code = args[1]
        string_value = args[2]
        if args[3].isdigit():
            key_value = int(args[3])

            if flag_code == 'e':
                run_coding(string_value, key_value)
            elif flag_code == 'd':
                run_coding(string_value, -key_value)
            else:
                print("Неправильный флаг шифрования!")
        else:
            print("Неправильный сдвиг!")
    else:
        print("Неправильное количество флагов!")
    return 0

def run_coding(s, key):
    global res
    for c in s:
        if c in lib_small_en:
            res += lib_small_en[(lib_small_en.index(c) + key) % len(lib_small_en)]
        elif c in lib_big_en:
            res += lib_big_en[(lib_big_en.index(c) + key) % len(lib_big_en)]
        elif c in lib_small_ru:
            res += lib_small_ru[(lib_small_ru.index(c) + key) % len(lib_small_ru)]
        elif c in lib_big_ru:
            res += lib_big_ru[(lib_big_ru.index(c) + key) % len(lib_big_ru)]
        else:
            res += c
    print("Обработанная строка: " + res)
    return res


if __name__ == '__main__':
    #main(sys.argv)
    print("Тест 1")
    main(['main.py', "124356", "abcde", "24315"])

    print("Тест 2")
    main(['main.py', "e", "abcdef 123 !@#$%^&*() ", "-5"])

    print("Тест 3")
    main(['main.py', "e", "abcdef ABCDEF 123 !@#$%^&*()", "5"])

    print("Тест 4")
    main(['main.py', "e", "", "erghwjr"])

    print("Тест 5")
    main(['main.py', "d", "abcdef АБВГД ц34п4п 4п п 3", "1"])

    print("Тест 6")
    main(['main.py', "d", "abcdef яяяяяя ааааа бббббб б б б  р р п п п а а  ", "2"])

    print("Тест 7")
    main(['main.py', "d", "abcdef", "3"])

