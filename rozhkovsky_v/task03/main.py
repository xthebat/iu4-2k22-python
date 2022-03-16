import sys
import re
from dataclasses import dataclass


class ParseArgsError(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        print("Example of input args: main.py <comments_from_youtube.txt> <real_and_youtube_names.csv>")
        return self.msg


class ParseFileError(Exception):
    def __init__(self, msg: str, file_name=None, line=-1):
        self.msg = msg
        self.file_name = file_name
        self.line = line

    def __str__(self):
        if self.file_name:
            return f"{self.msg} in {self.file_name}:{self.line}."
        else:
            return self.msg

@dataclass
class Name:
    youtube: str
    real: str = None
    github: str = None


class User:

    def __init__(self, name: Name, comments: list):
        self.name = name
        self.comments = comments

    def add_comment(self, comment: str):
        self.comments.append(comment)

    def count_of_comments(self) -> int:
        return len(self.comments)

    def print(self):
        print(self.name.real, "( aka", self.name.youtube, ") wrote", self.count_of_comments(), "comments:")
        for comment in self.comments:
            print(" -", comment)


# Производим парсинг по файлу с коментариями
def parse(file_name: str) -> dict:
    users_dict = dict()
    try:
        file = open(file_name, "rt", encoding='utf-8')
    except PermissionError:
        raise ParseFileError("Permission denied")
    except FileNotFoundError:
        raise ParseFileError(f"File {file_name} not found")

    strings = file.read().split("\n\n")
    file.close()

    line_index = 1
    for name_and_comment in strings:
        name_and_comment = name_and_comment.splitlines()
        if len(name_and_comment) < 2:
            raise ParseFileError("User and comment are separated by new_line", file_name, line_index)
        if len(name_and_comment) > 2:
            raise ParseFileError("Excess new line", file_name, line_index)

        yt_name = name_and_comment[0]
        comment = name_and_comment[1]
        name = Name(yt_name)
        new_user = User(name, list())
        user = users_dict.setdefault(yt_name, new_user)
        user.add_comment(comment)
        line_index += 3

    return users_dict


# производим парсинг по файлу с коментариями , используя список имён
def parse_using_names(file_name: str, names_list: list) -> dict:
    users_dict = dict()
    try:
        file = open(file_name, "rt", encoding='utf-8')
    except PermissionError:
        raise ParseFileError("Permission denied")
    except FileNotFoundError:
        raise ParseFileError(f"File {file_name} not found")

    text = file.read()
    file.close()

    for name in names_list:
        yt_name = name.youtube
        if yt_name == "":
            continue
        regex = re.findall(f"{yt_name}\n(.+)", text)
        if "" in regex:
            raise ParseFileError(f"User {yt_name} are separated from coment by new_line")
        user = User(name, regex)
        users_dict[yt_name] = user

    return users_dict


# парсинг списка имен из csv файла
def parse_from_csv(file_name: str) -> list:
    names_list = list()
    try:
        file = open(file_name, "rt", encoding='utf-8')
    except PermissionError:
        raise ParseFileError("Permission denied")
    except FileNotFoundError:
        raise ParseFileError(f"File {file_name} not found")

    text = file.read()
    file.close()

    line_index = 2

    for line in text.split("\n")[1:]:
        line = line.split(",")
        if len(line) < 4:
            raise ParseFileError("Count of fields less than 4", file_name, line_index)

        real_name = line[1]
        git_line = line[2].split("/")
        yt_name = line[3]
        if real_name == "" or git_line == "" or yt_name == "":
            raise ParseFileError("Empty fields", file_name, line_index)
        if len(git_line) != 4:
            raise ParseFileError("Invalid github link", file_name, line_index)
        git_name = git_line[3]
        name = Name(yt_name, real_name, git_name)
        names_list.append(name)
        line_index += 1

    return names_list


def main(args: list):

    if len(args) != 3:
        raise ParseArgsError(f"Invalid count of arguments({len(args) - 1} != 2).")

    csv_file = args[2]
    names_file = args[1]

    if not names_file.endswith(".txt"):
        raise ParseArgsError(f"Invalid names file format! {names_file} is not .txt file.")

    if not csv_file.endswith(".csv"):
        raise ParseArgsError(f"Invalid csv file format! {csv_file} is not .csv file.")

    # 1. Формируем список имён
    names_list = parse_from_csv(csv_file)

    # 2. По каждому имени собираем коменты
    # users_dict = parse_using_names(names_file, names_list)

    # Или собираем чисто из файла (чисто по условию тз, вариант 2)
    users_dict = parse(args[1])

    # 3. Печатаем
    for user in users_dict.values():
        user.print()


if __name__ == '__main__':
    # args error test
    main(["main.py", "test.txt"])  # invalid count
    main(["main.py", "file.csv", "file.txt"])  # invalid format
    main(["main.py", "file.csvtxt", "321.csv"])  # invalid format
    # parse error test
    main(["main.py", "test1.txt", "file.csv"])  # user and comment are separated by \n
    main(["main.py", "test2.txt", "file.csv"])  # excess \n
    main(["main.py", "test.txt", "file1.csv"])  # empty fields
    main(["main.py", "test.txt", "file2.csv"])  # invalid github link
    main(["main.py", "test.txt", "file3.csv"])  # empty fields
    # normal
    main(["main.py", "test.txt", "file.csv"])
