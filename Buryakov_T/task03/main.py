ZERO_WIDTH_SPACE = '\u200b'


class ParserYtError(Exception):

    def __init__(self, value):
        self.value = value


class ParserCsvError(Exception):

    def __init__(self, value):
        self.value = value


class IncorrectValueInFile(Exception):

    def __init__(self, file, string, index):
        self.name_of_file = file
        self.string = string
        self.index = index


class IncorrectValueInCSV(Exception):

    def __init__(self, file, string, index):
        self.name_of_file = file
        self.string = string
        self.index = index


def parser_yt_comments(name_of_file: str) -> dict:
    try:
        with open(name_of_file, 'rt') as file:
            sorted_comments = {}
            f = file.read().split('\n\n\n')
            for i, line in enumerate(f):
                name_and_comment = line.split('\n')
                value = sorted_comments.setdefault(name_and_comment[0], list())
                value.append(name_and_comment[1].replace(ZERO_WIDTH_SPACE, ''))
        return sorted_comments
    except FileNotFoundError:
        raise ParserYtError(name_of_file)
    except IndexError:
        raise IncorrectValueInFile(name_of_file, line, i*4+1)


def bond_name_nickname(name_of_file: str, dict_with_nick: dict) -> dict:
    try:
        dict_of_bonds = {}
        with open(name_of_file, 'rt') as file:
            for i, line in enumerate(file):
                new_line = line.split(',')
                if new_line[3] in dict_with_nick:
                    dict_of_bonds.setdefault(new_line[3], new_line[1])
                    if dict_of_bonds[new_line[3]] == "":
                        raise IncorrectValueInCSV(name_of_file, new_line[3], i+1)
        return dict_of_bonds
    except FileNotFoundError:
        raise ParserCsvError(name_of_file)


def print_info(sorted_comments: dict, bonds: dict) -> list:
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
        print_info(sorted_comments, dict_of_bonds)
    except ParserYtError as error:
        print(f"This file: '{error.value}' is not exist")
    except ParserCsvError as error:
        print(f"This file: '{error.value}' is not exist")
    except IncorrectValueInFile as error:
        print(f"Parser YouTube comments in file: '{error.name_of_file}' is not working with: '{error.string}' "
              f"in line: '{error.index}'")
    except IncorrectValueInCSV as error:
        print(f"False value in '{error.name_of_file}' with '{error.string}' in line '{error.index}'")


if __name__ == '__main__':
    main(["main.py", "MLNI Group.csv", "Comments.txt"])
    # main(["main.py", "MLNI Group.csv", "Comments bad.txt"])
    # main(["main.py", "MLNI Group bad.csv", "Comments.txt"])
