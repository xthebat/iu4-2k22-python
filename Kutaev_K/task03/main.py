import sys
from typing import List
from task03.classes import FileContentError, FileExtensionError
from task03.functions import check_args, parse_chat, parse_table, print_report


def main(args: List[str]) -> int:
    if len(args) < 2:
        sys.exit(f"Not enough args\n"
                 f"Usage: main.py [chat log file] [users table]")

    users_table: str = args[2]
    chat_file: str = args[1]

    try:
        check_args(chat_file, users_table)
        users_comm_dict: dict = parse_chat(chat_file)
        users_nick_dict: dict = parse_table(users_table)
    except FileNotFoundError as error:
        sys.exit(f"File '{error}' does not exist")
    except FileExtensionError as error:
        sys.exit(f"File '{error.file}' has wrong extension\n"
                 f"Extension should be '{error.true_extension}'")
    except EOFError as error:
        sys.exit(f"File '{error}' is empty")
    except FileContentError as error:
        sys.exit(f"File '{error.file}' has wrong data in line {error.line}")
    except PermissionError as error:
        sys.exit(f"You do not have permission to the '{error}' file")

    print_report(users_comm_dict, users_nick_dict)

    return 0


if __name__ == '__main__':
    main(["main.py", "chat1.txt", "table.csv"])
    # main(["main.py", "chat1.txt"])
    # main(["main.py", "chat2.txt1", "table.csv"])
    # main(["main.py", "chat3.txt", "table.csv"])
    # main(["main.py", "chat4.txt", "table.csv"])
