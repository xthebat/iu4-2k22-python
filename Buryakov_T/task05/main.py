import json
from typing import List

from CS_stats import Round, Match, Kill


def main():
    with open("1-bc6f4da7-e96b-4070-9a66-6392718d3ba6-1-1.json", "rt") as file:
        text = file.read()
        data = json.loads(text)

    match = Match.from_data(data)
    match.print_statistics()
    match.print_statistics_in_file()


if __name__ == '__main__':
    main()
