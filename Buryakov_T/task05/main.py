import json
from typing import List

from CS_stats import Round, Match


def main():
    with open("1-266bdc4c-3672-4cd5-bc97-b79c6c1e4d6a-1-1.json", "rt") as file:
        text = file.read()
        data = json.loads(text)

    match = Match.from_data(data)
    match.print()


if __name__ == '__main__':
    main()
