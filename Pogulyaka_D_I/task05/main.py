import json
import os
from typing import Iterable, List

from demo import Match


def main():
    with open("1-bc6f4da7-e96b-4070-9a66-6392718d3ba6-1-1.json", "rt") as file:
        text = file.read()
        data = json.loads(text)

    match = Match.from_data(data)
    match.players_print()
    match.match_print()


if __name__ == '__main__':
    main()
