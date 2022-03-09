import sys
import re


class Name:

    def __init__(self, real: str, youtube: str, github: str):
        self.real = real
        self.youtube = youtube
        self.github = github


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


def search_by_name(users_list: list, yt_name: str):
    for user in users_list:
        if user.name.youtube == yt_name:
            return user
    return None


# Производим парсинг по файлу с коментариями
def parse(file_name: str) -> list:
    users_list = list()
    file = open(file_name, "r", encoding='utf-8')
    text = file.read().split("\n")

    for i in range(0, len(text), 3):
        yt_name = text[i]
        comment = text[i+1]
        user = search_by_name(users_list, yt_name)
        if user is None:
            name = Name("None", yt_name, "None")
            user = User(name, list())
            users_list.append(user)
        user.add_comment(comment)

    file.close()
    return users_list


# производим парсинг по файлу с коментариями , используя список имён
def parse_use_names(file_name: str, names_list: list) -> list:
    users_list = list()
    file = open(file_name, "r", encoding='utf-8')
    text = file.read()
    for name in names_list:
        yt_name = name.youtube
        if yt_name == "":
            continue
        regex = re.findall(f"{yt_name}\n(.+)", text)
        user = User(name, regex)
        users_list.append(user)

    file.close()
    return users_list


# парсинг списка имен из csv файла
def parse_from_csv(file_name: str) -> list:
    names_list = list()
    file = open(file_name, "r", encoding='utf-8')

    text = file.read()
    for line in text.split("\n")[1:]:
        line = line.split(",")
        real_name = line[1]
        regex = re.search(r"github\.com/(.+)", line[2])
        if regex is None:
            git_name = ""
        else:
            git_name = regex.group(1)
        yt_name = line[3]
        name = Name(real_name, yt_name, git_name)
        names_list.append(name)

    file.close()
    return names_list


def main(args: list):

    # 1. Формируем список имён
    names_list = parse_from_csv(args[2])

    # 2. По каждому имени собираем коменты
    users_list = parse_use_names(args[1], names_list)

    # Или собираем чисто из файла (по условию)
    # users_list = parse(args[1])

    # 3. Печатаем
    for user in users_list:
        user.print()


if __name__ == '__main__':
    # main(["main.py", "test.txt", "file.csv"])
    main(sys.argv)
