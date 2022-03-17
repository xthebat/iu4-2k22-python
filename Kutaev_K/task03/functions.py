from os.path import exists
from task03.configs import *
from task03.classes import FileContentError
from task03.classes import FileExtensionError


def check_comment(chat_file: str, chat_file_lines: list, idx: int):
    if chat_file_lines[idx] == '\n':
        raise FileContentError(chat_file, idx)
    if chat_file_lines[idx + 1] == '\n':
        raise FileContentError(chat_file, idx+1)
    if len(chat_file_lines) - idx > 2:
        if chat_file_lines[idx + 2] != '\n':
            raise FileContentError(chat_file, idx+2)


def parse_chat(chat_file: str) -> dict:
    with open(chat_file, encoding=ENCODING) as chat_file_read:
        chat_file_lines: list = chat_file_read.readlines()

    if not chat_file_lines:
        raise EOFError(chat_file)

    users_comm_dict: dict = {}
    for idx in range(0, len(chat_file_lines), COMMENTS_STEP):
        check_comment(chat_file, chat_file_lines, idx)

        username: str = chat_file_lines[idx].removesuffix('\n')
        if not users_comm_dict.get(username):
            users_comm_dict.update({username: []})
        users_comm_dict[username].append(chat_file_lines[idx + 1].removesuffix('\n'))

    return users_comm_dict


def parse_table(users_table: str) -> dict:
    with open(users_table, 'r', encoding=ENCODING) as table_file_read:
        table_file_lines: list = table_file_read.readlines()

    if not table_file_lines:
        raise EOFError(users_table)

    users_nick_dict: dict = {}
    for line in table_file_lines:
        list_line: list = line.split(',')

        if list_line[NUMBER_CELL].isdigit():
            if list_line[REAL_NAME_CELL] == '':
                raise FileContentError(users_table, int(line))

            if list_line[YT_NICK_CELL] != '':
                users_nick_dict.update({list_line[YT_NICK_CELL]: list_line[REAL_NAME_CELL]})
    return users_nick_dict


def print_report(users_comm_dict: dict, users_nick_dict: dict):
    for key, value in users_comm_dict.items():
        yt_username: str = key
        real_name: str = users_nick_dict.get(key)
        if not real_name:
            real_name = "Unknown"
        comm_number: int = len(value)
        symbols_number: int = 0
        for comment in value:
            symbols_number += len(comment)

        print(f"{yt_username} aka {real_name} printed {comm_number} comments, "
              f"which contains {symbols_number} symbol. Here they comes:")
        for comment in value:
            print(f"-> {comment}")


def check_args(chat_file: str, users_table: str):
    if not exists(chat_file):
        raise FileNotFoundError(chat_file)

    extension = chat_file.split('.')[-1]
    if extension != CHAT_EXTENSION:
        raise FileExtensionError(CHAT_EXTENSION, chat_file)

    if not exists(users_table):
        raise FileNotFoundError(users_table)

    extension = users_table.split('.')[-1]
    if extension != USERS_TABLE_EXTENSION:
        raise FileExtensionError(USERS_TABLE_EXTENSION, users_table)
