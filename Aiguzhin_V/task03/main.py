from collections import defaultdict


def parse_chat() -> dict:
    with open("chat.txt", "rt", encoding="UTF-8") as file:
        file_content = file.read()
        data = [lines.replace('\u200b', '').split("\n") for lines in file_content.split("\n\n")]
        user_comments = defaultdict(list)
        for value in data:
            user_comments[value[0]].append(value[1])
    return dict(user_comments)


def parse_nicknames() -> dict:
    with open("ИУ4 - МЛНИ - 2022.csv", "rt") as file:
        file_content = file.read()
        data = [line.split(',') for line in file_content.split("\n")]
        # Presuming the first line is a header, get indices of required columns
        column_index = {column: index for index, column in enumerate(data[0]) if column in ("Номер", "ФИО", "Youtube")}
        # Get lines with students by filtering by value of "Номер" column
        lines_with_index = [line for line in data if line[column_index["Номер"]].isdigit()]
        # Only people with nicknames make it to the final result
        parsed_data = {name_nickname[column_index["Youtube"]]: name_nickname[column_index["ФИО"]] for name_nickname in
                       lines_with_index if name_nickname[column_index["Youtube"]]}
    return parsed_data


def print_stats(comments: dict, real_names: dict) -> None:
    for nickname, name in real_names.items():
        for viewer, value in comments.items():
            if nickname == viewer:
                symbols = sum(len(comment) for comment in value)
                print(f"'{nickname}' aka {name} with {len(value)} comment(s) and {symbols} symbol(s):")
                for comment in value:
                    print(comment)
                print('\n')
    return None


def main(args: list[str]) -> None:
    user_comments = parse_chat()
    nickname_name = parse_nicknames()
    print_stats(user_comments, nickname_name)
    return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(["main.py", "...", "..."])
    main(["main.py", "...", "..."])
    main(["main.py", "...", "..."])
