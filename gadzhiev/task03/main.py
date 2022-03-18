import sys

ZERO_WIDTH_SPACE = "\u200b"
NIKCNAME_POSITION_IN_CSV = 3
NAME_POSITION_IN_CSV = 1
ITERATION_IN_TXT = 4


class CsvTypeError(Exception):
    def __init__(self, value):
        self.value = value


class TxtTypeError(Exception):
    def __init__(self, value):
        self.value = value


class InTxtError(Exception):
    def __init__(self, value, index):
        self.value = value
        self.index = index


class InCsvError(Exception):
    def __init__(self, value, index):
        self.value = value
        self.index = index


class FileError(Exception):
    def __init__(self, value):
        self.value = value


def read_file(arg: str) -> str:
    try:
        with open(arg, "r", encoding="utf-8") as file:
            chat = file.read()
    except FileNotFoundError:
        raise FileError(arg)
    else:
        return chat


def parse_txt_file(text: str, name: str) -> dict:
    chat = text.split("\n\n\n")
    dict_of_comments = {}
    for index, element in enumerate(chat):
        elem = element.split("\n")
        list_of_comm = dict_of_comments.setdefault(elem[0], list())
        try:
            list_of_comm.append(elem[1].replace(ZERO_WIDTH_SPACE, ""))
        except IndexError:
            raise InTxtError(elem[0], index)
        dict_of_comments[elem[0]] = list_of_comm
    if len(dict_of_comments) <= 1:
        raise TxtTypeError(name)
    else:
        return dict_of_comments


def parse_csv_file(text: str, name: str) -> list:
    try:
        table = text.split("\n")
        name_nickname_list = []
        for element in table:
            list_element = element.split(",")
            name_nickname_list.append([list_element[NIKCNAME_POSITION_IN_CSV],
                                       list_element[NAME_POSITION_IN_CSV]])
        return name_nickname_list
    except IndexError:
        raise CsvTypeError(name)


def build_dict_of_names(dict_of_comments: dict, name_nickname_list: list) -> dict:
    name_nickname_dict = {}
    for index, elem in enumerate(name_nickname_list):
        if elem[0] in dict_of_comments:
            if elem[1] == "":
                raise InCsvError(elem[0], index + 1)
            name_nickname_dict[elem[0]] = elem[1]
    return name_nickname_dict


def print_information(dict_of_comment: dict, dict_of_nicknames: dict) -> None:
    for key_el, value_el in dict_of_nicknames.items():
        print(f"Статистика по {value_el} ({key_el}):")
        for key, value in dict_of_comment.items():
            if key == key_el:
                print(f"Количество комментариев = {len(value)}")
                print(f"Количество символов = {len(''.join(value))}")
                for ind, elem in enumerate(value):
                    print(f"{ind + 1}-й комментарий: {elem}")
                print("." * 50)


def main(args: list):
    try:
        dict_of_comments = parse_txt_file(read_file(args[1]), args[1])
        dict_of_nicknames = build_dict_of_names(dict_of_comments,
                                                parse_csv_file(read_file(args[2]), args[2]))
        print_information(dict_of_comments, dict_of_nicknames)
    except FileError as error:
        print(f"Файл '{error.value}' не найден\n")
    except CsvTypeError as error:
        print(f"Ожидался csv-файл\n"
              f"Проверьте расширение файла: {error.value}\n")
    except TxtTypeError as error:
        print(f"Ожидался txt-файл\n"
              f"Проверьте расширение файла: {error.value}\n")
    except InTxtError as error:
        print(f"Ошибка в .txt файле в строке: '{error.value}'\n"
              f"Номер строки: {error.index * ITERATION_IN_TXT + 1}\n")
    except InCsvError as error:
        print(f"Ошибка в .csv файле в строке: '{error.index}'\n"
              f"У {error.value} нет YouTube-никнейма\n")


if __name__ == '__main__':
    main(sys.argv)
    main(["main.py", "Comments.txt",  "score.csv"])         # проверка FileError
    main(["main.py", "scoreboard.csv", "scoreboard.csv"])   # проверка TxtTypeError
    main(["main.py", "chat.txt", "chat.txt"])               # проверка CsvTypeError
    main(["main.py", "err_chat.txt", "scoreboard.csv"])     # проверка InTxtError
    main(["main.py", "chat.txt", "err_scoreboard.csv"])     # проверка InCsvError

