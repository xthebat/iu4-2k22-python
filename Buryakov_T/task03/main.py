import sys


class ParserYtError(Exception):

    def __init__(self, value, string):
        self.value = value
        self.string = string


class ParserCsvError(Exception):

    def __init__(self, value, string):
        self.value = value
        self.string = string


class IncorrectValueInFile(Exception):

    def __init__(self, file, string):
        self.name_of_file = file
        self.string = string


def parser_yt_comments(name_of_file: str) -> dict:
    try:
        with open(name_of_file, 'r') as file:
            sorted_comments = {}
            for line in file:
                if line not in '\n' and '\u200b' not in line:
                    nickname = line.replace('\n', '')
                elif line not in '\n' and '\u200b' in line:
                    if nickname in sorted_comments.keys():
                        sorted_comments[nickname].append(line.replace('\n', '').replace('\u200b', ''))
                    else:
                        sorted_comments[nickname] = [line.replace('\n', '').replace('\u200b', '')]
        return sorted_comments
    except FileNotFoundError:
        raise ParserYtError(name_of_file, sys.exc_info()[2].tb_lineno)


def bond_name_nickname(name_of_file: str, dict_with_nick) -> dict:
    try:
        dict_of_bonds = {}
        with open(name_of_file, 'r') as file:
            for line in file:
                new_line = line.split(',')
                if new_line[3] in dict_with_nick.keys():
                    dict_of_bonds[new_line[3]] = new_line[1]
        return dict_of_bonds
    except FileNotFoundError:
        raise ParserCsvError(name_of_file, sys.exc_info()[2].tb_lineno)
        pass


def stream_info(sorted_comments: dict, bonds: dict) -> list:
    full_info = []
    for key, values in sorted_comments.items():
        real_name = bonds[key]
        number_of_comments = len(sorted_comments[key])
        number_of_symbols = 0
        for item in range(number_of_comments):
            number_of_symbols += len(sorted_comments[key][item])
        full_info.append([key, real_name, number_of_comments, number_of_symbols, values])
    for val in full_info:
        print(f"Nickname: {val[0]}, Name: {val[1]}, Number of comments: {val[2]}, Number of symbols: {val[3]}")
        for i, item in enumerate(val[4]):
            print(f"Comment {i+1}: {item}")
        print("-"*130)
    return full_info


def main(args: list):
    try:
        sorted_comments = parser_yt_comments(args[2])
        dict_of_bonds = bond_name_nickname(args[1], sorted_comments)
        stream_info(sorted_comments, dict_of_bonds)
    except ParserYtError as error:
        print(f"This file: '{error.value}' is not exist in line {error.string}")
    except ParserCsvError as error:
        print(f"This file: '{error.value}' is not exist in line {error.string}")
    except IncorrectValueInFile as error:
        print(f"Parser YouTube comments in file: '{error.name_of_file}' is not working with line: '{error.string}'")


if __name__ == '__main__':
    main(["main.py", "MLNI Group.csv", "Comments.txt"])

