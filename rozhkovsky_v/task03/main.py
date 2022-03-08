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

    def count_of_comments(self):
        return len(self.comments)

    def print(self):
        print(self.name.real, "( aka", self.name.youtube, ") wrote", self.count_of_comments(), "comments:")
        for comment in self.comments:
            print(" -", comment)


def main(args: list):

    names_list = list()
    users_list = list()

    file_yt = open(args[1], "r", encoding='utf-8')
    file_csv = open(args[2], "r", encoding='utf-8')

    # 1. Формируем список имён
    text = file_csv.read()
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

    # 2. По каждому имени собираем коменты
    text = file_yt.read()
    for name in names_list:
        yt_name = name.youtube
        if yt_name == "":
            continue
        regex = re.findall(f"{yt_name}\n(.+)", text)
        user = User(name, regex)
        users_list.append(user)

    # 3. Печатаем
    for user in users_list:
        user.print()

    file_yt.close()
    file_csv.close()


if __name__ == '__main__':
    # main(["main.py", "test.txt", "file.csv"])
    main(sys.argv)
