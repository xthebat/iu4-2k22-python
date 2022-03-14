from os.path import exists
import sys
from task03.configs import *
from task03.classes import FileContentError
from task03.classes import FileExtensionError


def check_comment(chat_file_lines: list, idx: int) -> int:
    if chat_file_lines[idx] == '\n':
        return idx
    if chat_file_lines[idx + 1] == '\n':
        return idx + 1
    if len(chat_file_lines) - idx > 2:
        if chat_file_lines[idx + 2] != '\n':
            return idx + 2
    return GOOD_COMM


def parse_chat(chat_file: str) -> dict:
    try:
        chat_file_read = open(chat_file, encoding=ENCODING)
    except PermissionError as error:
        sys.exit(f"You do not have permission to the '{error}' file ")
    chat_file_lines: list = chat_file_read.readlines()

    if not chat_file_lines:
        raise EOFError(chat_file)

    users_comm_dict: dict = {}
    for idx in range(0, len(chat_file_lines), COMMENTS_STEP):
        res_check = check_comment(chat_file_lines, idx)
        if res_check != GOOD_COMM:
            raise FileContentError(chat_file, res_check)

        username: str = chat_file_lines[idx].removesuffix('\n')
        if not users_comm_dict.get(username):
            users_comm_dict.update({username: []})
        users_comm_dict[username].append(chat_file_lines[idx + 1].removesuffix('\n'))

    chat_file_read.close()
    return users_comm_dict


def parse_table(users_table: str) -> dict:
    try:
        table_file_read = open(users_table, 'r', encoding=ENCODING)
    except PermissionError as error:
        sys.exit(f"You do not have permission to the '{error}' file ")
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

    chat_file_list: list = list(chat_file)
    extension = chat_file_list[-EXTENSION_LEN:]
    if ''.join(extension) != CHAT_EXTENSION:
        raise FileExtensionError(CHAT_EXTENSION, chat_file)

    if not exists(users_table):
        raise FileNotFoundError(users_table)

    users_table_list: list = list(users_table)
    extension = users_table_list[-EXTENSION_LEN:]
    if ''.join(extension) != USERS_TABLE_EXTENSION:
        raise FileExtensionError(USERS_TABLE_EXTENSION, users_table)
