import sys
import re
from dataclasses import dataclass


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

    file = open(file_name, "rt", encoding='utf-8')
    strings = file.read().split("\n\n")
    file.close()

    for name_and_comment in strings:
        name_and_comment = name_and_comment.splitlines()
        yt_name = name_and_comment[0]
        comment = name_and_comment[1]
        name = Name(yt_name)
        new_user = User(name, list())
        user = users_dict.setdefault(yt_name, new_user)
        user.add_comment(comment)

    return users_dict


# производим парсинг по файлу с коментариями , используя список имён
def parse_using_names(file_name: str, names_list: list) -> dict:
    users_dict = dict()
    file = open(file_name, "rt", encoding='utf-8')
    text = file.read()
    file.close()
    for name in names_list:
        yt_name = name.youtube
        if yt_name == "":
            continue
        regex = re.findall(f"{yt_name}\n(.+)", text)
        user = User(name, regex)
        users_dict[yt_name] = user

    return users_dict


# парсинг списка имен из csv файла
def parse_from_csv(file_name: str) -> list:
    names_list = list()
    file = open(file_name, "rt", encoding='utf-8')
    text = file.read()
    file.close()

    for line in text.split("\n")[1:]:
        line = line.split(",")
        real_name = line[1]
        git_line = line[2].split("/")
        if len(git_line) != 4:
            git_name = ""
        else:
            git_name = git_line[3]
        yt_name = line[3]
        name = Name(yt_name, real_name, git_name)
        names_list.append(name)

    return names_list


def main(args: list):

    # 1. Формируем список имён
    names_list = parse_from_csv(args[2])

    # 2. По каждому имени собираем коменты
    users_dict = parse_using_names(args[1], names_list)

    # Или собираем чисто из файла (чисто по условию тз, вариант 2)
    # users_dict = parse(args[1])

    # 3. Печатаем
    for user in users_dict.values():
        user.print()


if __name__ == '__main__':
    # main(["main.py", "test.txt", "file.csv"])
    main(sys.argv)
