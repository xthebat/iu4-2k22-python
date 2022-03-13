import sys

AVA_IN_UTF = "\u200b"
NIKCNAME_POSITION = 3
NAME_POSITION = 1


class FileError(Exception):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class TxtError(Exception):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class CsvError(Exception):
    def __init__(self, value, line):
        self.value = value
        self.line = line


def read_file(arg: str) -> list:
    try:
        with open(arg, "r", encoding="utf-8") as file:
            chat = file.read()
            chat_list = chat.split("\n")
    except FileNotFoundError:
        raise FileError(arg, sys.exc_info()[2].tb_lineno)
    else:
        return chat_list


def parse_txt_file(text: list) -> dict:
    dict_of_comments = {}
    for ind, elem in enumerate(text):
        if elem != "" and AVA_IN_UTF not in elem:
            dict_of_comments[elem] = []
    for ind, elem in enumerate(text):
        if elem != "" and AVA_IN_UTF not in elem:
            list_of_comm = dict_of_comments.get(elem)
            list_of_comm.append(text[ind + 1].replace(AVA_IN_UTF, ""))
    return dict_of_comments


def parse_csv_file(dict_of_comments: dict, list_from_csv: list) -> dict:
    name_nickname_dict = dict_of_comments.fromkeys(dict_of_comments, "")
    for elem in name_nickname_dict.keys():
        for unit in list_from_csv:
            list_unit = unit.split(",")
            if elem == list_unit[NIKCNAME_POSITION]:
                name_nickname_dict[elem] = list_unit[NAME_POSITION]
    return name_nickname_dict


def print_information(dict_of_comment: dict, dict_of_nicknames: dict) -> None:
    for key_el, value_el in dict_of_nicknames.items():
        print(f"Статистика по {value_el} ({key_el}):")
        for key, value in dict_of_comment.items():
            if key == key_el:
                print(f"Количество комментариев = {len(value)}")
                print(f"Количество символов = {len(''.join(value))}")
                for ind, elem in enumerate(value):
                    print(f"{ind+1}-й комментарий: {elem}")
                print("."*50)


def main(args: list):
    try:
        try:
            comments = parse_txt_file(read_file(args[1]))
        except IndexError:
            raise TxtError(args[1], sys.exc_info()[2].tb_lineno)
        try:
            nicknames = parse_csv_file(comments, read_file(args[2]))
        except IndexError:
            raise CsvError(args[1], sys.exc_info()[2].tb_lineno)
        print_information(comments, nicknames)
    except FileError as error:
        print(f"Файл '{error.value}' не найден. Строка ошибки: '{error.line}'")
    except TxtError as error:
        print(f"Данная функция принимает только .txt файлы\n"
              f"Файл '{error.value}' не подходит. Строка ошибки: '{error.line}'")
    except CsvError as error:
        print(f"Данная функция принимает только .csv файлы\n"
              f"Файл '{error.value}' не подходит. Строка ошибки: '{error.line}'")


if __name__ == '__main__':
    main(sys.argv)
    # main(["main.py", "Comments.txt",  "score.csv"])  # проверка наличия файла
    # main(["main.py", "scoreboard.csv", "Comments.txt"])  # проверка корректности типа файла
