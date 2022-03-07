import sys
import os


def pars_user_line(str_line: str) -> (str, str):
    index = [i for i, char in enumerate(str_line) if char == ";"]
    yt_name = str_line[index[2] + 1:index[3]]
    real_name = str_line[index[0] + 1:index[1]]
    return yt_name, real_name


def gen_user_dict(path_file: str) -> dict:
    list_lines = list(filter(lambda it: it[0].isdigit(), open(path_file, "rt").readlines()))
    dict_result = dict(map(pars_user_line, list_lines))
    if "" in dict_result:
        del dict_result[""]
    return dict_result


def gen_chat_dict(path_file: str) -> dict:
    list_message = [it.split("\n?") for it in open(path_file, "rt").read().split("\n\n")]
    dict_result = dict()
    for it in list_message:
        dict_result.setdefault(it[0], list())
        dict_result[it[0]].append(it[1])
    return dict_result


def print_chat(user_dict: dict, chat_dict: dict):
    for item in chat_dict:
        print(item + " aka " + user_dict.get(item, "not declared"))
        print("    Кол-во сообщений: " + str(len(chat_dict[item])))
        print("    Кол-во символов: " + str(sum(map(len, chat_dict[item]))))
        for mess in chat_dict[item]:
            print(" -" + mess)
        print()


def main(args: list):

    if not os.path.exists(args[1]):
        sys.exit("User file is not exist")

    if not os.path.exists(args[2]):
        sys.exit("Chat file is not exist")

    if args[1][-4:] != ".csv":
        sys.exit("User file is not csv")

    if args[2][-4:] != ".txt":
        sys.exit("Chat file is not txt")

    user_dict = gen_user_dict(args[1])
    chat_dict = gen_chat_dict(args[2])
    print_chat(user_dict, chat_dict)


# chat file is txt in ANSI format


if __name__ == '__main__':
    # main(sys.argv)
    main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./chat.txt"])
    # main(["main.py", "./chat.txt", "./chat.txt"])
    # main(["main.py", "./ИУ4 - МЛНИ - 2022.csv", "./ИУ4 - МЛНИ - 2022.csv"])
