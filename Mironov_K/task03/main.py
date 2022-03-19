import sys
import os


class FileExtError(Exception):

    def __init__(self, file: str, ext: str):
        self.file = file
        self.ext = ext


class ParseError(Exception):

    def __init__(self, line: str):
        self.line = line


# По сути функция добавления имен пользователей дополнительная, поэтому при наличии ошибок вывожу пустой словарь


def parse_csv_file(path_file: str) -> list:
    if os.path.splitext(path_file)[1] != ".csv":
        raise FileExtError(path_file, "csv")
    list_lines = open(path_file, "rt").readlines()
    list_result = [it.split(";") for it in list_lines]
    return list_result


REAL_NAME_COLUMN = 1
YT_NAME_COLUMN = 3


def gen_user_dict(list_users: list) -> dict:
    dict_result = {}
    for it in list_users:
        try:
            if it[0].isdigit() and it[YT_NAME_COLUMN] != "":
                dict_result[it[YT_NAME_COLUMN]] = it[REAL_NAME_COLUMN]
        except IndexError:
            raise ParseError(it)
    # dict_result = {it[YT_NAME_COLUMN]: it[REAL_NAME_COLUMN]
                   # for it in list_users if it[0].isdigit() and it[YT_NAME_COLUMN] != ""}
    return dict_result


def gen_chat_dict(path_file: str) -> dict:
    if os.path.splitext(path_file)[1] != ".txt":
        raise FileExtError(path_file, "txt")
    list_chat = open(path_file, mode="rt", encoding="UTF-16").read().split("\n\n")
    for it in list_chat:
        if it.count("\n\u200b") != 1:
            raise ParseError(it)
    # Не придумал ничего лучше для исключения чем прогонка через фор
    # list_message = [it.split("\n\u200b") for it in list_chat if it.count("\n\u200b") == 1]
    list_message = [it.split("\n\u200b") for it in list_chat]
    # При копировании чата с ютуба перед комметарием есть дополнительный символ юникода: пробел нулевой ширины
    dict_result = dict()
    for it in list_message:
        yt_name = it[0]
        dict_result.setdefault(yt_name, list())
        dict_result[yt_name].append(it[1])
    return dict_result


def print_chat(user_dict: dict, chat_dict: dict):
    for yt_name in chat_dict:
        real_name = user_dict.get(yt_name, "not declared")
        print(f"\n{yt_name} aka {real_name}")
        print(f"\tКол-во сообщений: {len(chat_dict[yt_name])}")
        print(f"\tКол-во символов: {sum(map(len, chat_dict[yt_name]))}")
        for mess in chat_dict[yt_name]:
            print(f" -{mess}")


def main(args: list):
    path_file_users = args[1]
    path_file_chat = args[2]

    try:
        list_parse_users = parse_csv_file(path_file_users)
    except FileNotFoundError as error:
        print(error)
        user_dict = {}
    except FileExtError as error:
        print(f"File extention error: {error.file} is not {error.ext}")
        user_dict = {}
    else:
        try:
            user_dict = gen_user_dict(list_parse_users)
        except ParseError as error:
            print(f"Error format REAL_NAME_COLUMN = {REAL_NAME_COLUMN} YT_NAME_COLUMN ="
                  f" {YT_NAME_COLUMN} file {path_file_users} in line:\n {error.line}")
            user_dict = {}

    try:
        chat_dict = gen_chat_dict(path_file_chat)
    except FileNotFoundError as error:
        sys.exit(error)
    except FileExtError as error:
        sys.exit(f"File extention error: {error.file} is not {error.ext}")
    except UnicodeDecodeError as error:
        sys.exit(f"File {path_file_chat} codec error: {error}")
    except ParseError as error:
        sys.exit(f"Error format file {path_file_chat} in message:\n {error.line}")

    print_chat(user_dict, chat_dict)


if __name__ == '__main__':
    # main(sys.argv)
    main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_ideal.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_codecUTF8.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_codecANSI.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_messageerror.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_messageerror2.txt"])
    # main(["main.py", "./chat.txt", "./chat_ideal.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./ИУ4 - МЛНИ - 2022.csv"])
