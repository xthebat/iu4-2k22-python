import json
import os
from typing import Iterable, List

from demo import Round, Match, Player


def main():
    with open("temp/1-266bdc4c-3672-4cd5-bc97-b79c6c1e4d6a-1-1.json", "rt") as file:
        text = file.read()
        data = json.loads(text)

    match = Match.from_data(data)
    match.players_print()


if __name__ == '__main__':
    main()
