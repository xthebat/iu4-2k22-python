import json
import os
import sys
from typing import Iterable, List

from demo import Round, Match, Player


def main(args: list):
    if len(args) > 1:
        with open(args[1], "rt") as file:
            text = file.read()
            data = json.loads(text)

        match = Match.from_data(data)
        match.players_print()

    else:
        print("\n--------- test2v2.json ---------")
        with open("temp/test2v2.json", "rt") as file:
            text = file.read()
            data = json.loads(text)

        match = Match.from_data(data)
        match.players_print()

        print("\n--------- test5v5.json ---------")

        with open("temp/test5v5.json", "rt") as file:
            text = file.read()
            data = json.loads(text)

        match = Match.from_data(data)
        match.players_print()


if __name__ == '__main__':
    main(sys.argv)

