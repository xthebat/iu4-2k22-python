import sys
import os


class FileExtError(Exception):

    def __init__(self, file: str, ext: str):
        self.file = file
        self.ext = ext


class ChatParseError(Exception):

    def __init__(self, line: str):
        self.line = line


# По сути функция добавления имен пользователей дополнительная, поэтому при наличии ошибок вывожу пустой словарь


def gen_user_dict(path_file: str) -> dict:
    try:
        if os.path.splitext(path_file)[1] != ".csv":
            raise FileExtError(path_file, "csv")
        list_lines = open(path_file, "rt").readlines()
    except FileNotFoundError as error:
        print(error)
        return {}
    except FileExtError as error:
        print(f"File extention error: {error.file} is not {error.ext}")
        return {}
    else:
        list_users = (it.split(";") for it in list_lines)
        dict_result = {it[3]: it[1] for it in list_users if it[0].isdigit() and it[3] != ""}
        return dict_result


def gen_chat_dict(path_file: str) -> dict:
    try:
        if os.path.splitext(path_file)[1] != ".txt":
            raise FileExtError(path_file, "txt")
        list_chat = open(path_file, mode="rt", encoding="UTF-16").read().split("\n\n")
        for it in list_chat:
            if it.count("\n\u200b") != 1:
                raise ChatParseError(it)
        # Не придумал ничего лучше для исключения чем прогонка через фор
        # list_message = [it.split("\n\u200b") for it in list_chat if it.count("\n\u200b") == 1]
        list_message = [it.split("\n\u200b") for it in list_chat]
        # При копировании чата с ютуба перед комметарием есть дополнительный символ юникода: пробел нулевой ширины
    except FileNotFoundError as error:
        sys.exit(error)
    except FileExtError as error:
        sys.exit(f"File extention error: {error.file} is not {error.ext}")
    except UnicodeDecodeError as error:
        sys.exit(f"File {path_file} codec error: {error}")
    except ChatParseError as error:
        sys.exit(f"Error format file {path_file} in message:\n {error.line}")
    else:
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
    user_dict = gen_user_dict(args[1])
    chat_dict = gen_chat_dict(args[2])
    print_chat(user_dict, chat_dict)


if __name__ == '__main__':
    # main(sys.argv)
     main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_ideal.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_codecUTF8.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_codecANSI.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_messageerror.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat_messageerror2.txt"])
    # main(["main.py", "./chat.txt", "./chat.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./ИУ4 - МЛНИ - 2022.csv"])
