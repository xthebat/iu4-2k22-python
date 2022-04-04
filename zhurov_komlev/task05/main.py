import json
import sys

from demo import MapStatistics


def main(args: list):
    if len(args) > 2:
        print_match(args[1], args[2])

    else:
        print_match("test2v2.json", "Team")
        print_match("test5v5.json", "K")


def print_match(match: str, sort: str):
    print("\n---------" + match + "---------")
    with open("temp/" + match, "rt") as file:
        text = file.read()
        data = json.loads(text)
    match = MapStatistics.from_data(data, sort)
    match.print_statistics()


if __name__ == '__main__':
    main(sys.argv)
