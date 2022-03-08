import os
import csv
import sys

CHAT_DIC = {}
SCOREBOARD_DIC = {}


def count_sym(keys) -> int:
    count = 0
    if keys in CHAT_DIC:
        for comments in CHAT_DIC[keys]:
            count += len(comments)

    return count


def chat_parse(file):
    chat_list = []
    for line in file:
        line = line.strip("\u200b\n")
        if len(line) != 0:
            chat_list.append(line)

    for i in range(len(chat_list)):
        if i % 2 == 0:
            if str(chat_list[i]) not in CHAT_DIC:
                CHAT_DIC[str(chat_list[i])] = list()

            CHAT_DIC[str(chat_list[i])].append(chat_list[i+1])


def scoreboard_parse(file):
    csvreader = csv.reader(file)
    next(csvreader)
    rows = []
    for row in csvreader:
        rows.append(row)

    for i in range(len(rows)):
        if rows[i][3] != "" and rows[i][1] != "":
            if str(rows[i][3]) not in SCOREBOARD_DIC:
                SCOREBOARD_DIC[str(rows[i][3])] = list()

            SCOREBOARD_DIC[str(rows[i][3])] = rows[i][1]


def print_data():
    data_dic = {}
    for keys in CHAT_DIC:
        if keys in SCOREBOARD_DIC:
            data_dic[keys] = list()
            data_dic[keys].append(len(CHAT_DIC[keys]))
            data_dic[keys].append(count_sym(keys))
            for comments in CHAT_DIC[keys]:
                data_dic[keys].append(comments)

    for keys, value in data_dic.items():
        print(keys, value[0], value[1])
        for comments in value[2:]:
            print(comments)


def check_command(args):
    if not args[0].endswith(".py"):
        sys.exit("First element is not a .py file")
    elif not args[1].endswith(".txt"):
        sys.exit("The second element is not a .txt file")
    elif not args[2].endswith(".csv"):
        sys.exit("The third element is not a .csv file")

    if not os.path.exists(args[0]):
        sys.exit("There is no such a .py file")
    elif not os.path.exists(args[1]):
        sys.exit("There is no such a .txt file")
    elif not os.path.exists(args[2]):
        sys.exit("There is no such a .csv file")


def main(args: list[str]):
    check_command(args)
    file = open(args[1], "r", encoding="utf-8")
    chat_parse(file)
    file.close()
    file = open(args[2], "r")
    scoreboard_parse(file)
    file.close()
    print_data()


if __name__ == '__main__':
    main(["main.py", "chat.txt", "scoreboard.csv"])
