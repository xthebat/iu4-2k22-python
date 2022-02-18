import sys
import os

# Вообще нужно эти данные передавать как путь к CSV файлику как минимум.
# Но c CSV я через пандас работаю, а тут его использовать не стоит думаю.
# А как максимум - читать из таблицы Sheets, но я делать это не хочу,
# потому что там дурацкий апи и вообще доступ редактора через апи нужен, вот!
aka_map_dict = {
    "Shadowk 1337": "Федоров Роман",
    "lalaa mala": "Смирнов Владислав",
    "CoraL77": "Кутаев Кирилл",
    "Обри": "Комлев Илья",
    "Konstantin Zhurov": "Журов Константин",
    "Meme Theme": "Василенко Никита",
    "AAAAAA": "AAAAAA",
}


def main(args: list):
    if len(args) > 1:
        if os.path.exists(args[1]):
            with open(args[1], "r", encoding="utf8") as input_file:
                data_raw = input_file.read()
            author_data_list = parse(data_raw)
            map_author_data_aka(author_data_list, aka_map_dict)
            output_string = ""
            for author_data in author_data_list:
                output_string += f"{author_data}\n"
                for i, comment in enumerate(author_data.comments):
                    output_string += f"[{i+1}] {comment}\n"
                output_string += "\n"
            if len(args) > 2:
                with open(args[2], 'w', encoding="utf8") as output_file:
                    output_file.write(output_string)
            else:
                print(output_string)

        else:
            print("Input file does not exist!")
    else:
        print("Invalid parameters!")
        print("Usage: python comments.py <input file> <output file - optional>")


class AuthorData:
    def __init__(self, author) -> None:
        self.author = author
        self.aka = None
        self.comments = []
        self.comments_count = 0
        self.symbols_count = 0

    def __str__(self) -> str:
        aka = "" if self.aka is None else f" aka {self.aka}"
        return f"{self.author}{aka} написал(а) {self.comments_count} шт. комментариев на {self.symbols_count} шт. символов"


def parse(data_raw: str) -> list:
    author_data_list = []
    comments_splitted = data_raw.strip().split('\n\n')
    for comment_raw in comments_splitted:
        comment_splitted = comment_raw.strip().split('\n')
        if len(comment_splitted) == 2:
            author, comment = comment_splitted
            author_data = next(
                (x for x in author_data_list if x.author == author), None)
            if author_data is None:
                author_data = AuthorData(author)
                author_data_list.append(author_data)
            author_data.comments.append(comment.strip())
            author_data.comments_count += 1
            author_data.symbols_count += len(comment)
    return author_data_list


def map_author_data_aka(author_data_list, aka_map_dict) -> None:
    for author_data in author_data_list:
        if author_data.author in aka_map_dict:
            author_data.aka = aka_map_dict[author_data.author]


if __name__ == "__main__":
    main(sys.argv)
