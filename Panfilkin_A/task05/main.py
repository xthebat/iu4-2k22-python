import json
import sys

from CounterStrikeGO import Match


def main(args) -> None:
    if len(args) == 0:
        raise Exception("Excepted filename argument")
    filename = args[0]
    with open(filename, "r") as f:
        match_dict = json.load(f)

    match = Match.from_dict(match_dict)
    match.print_statistics()


if __name__ == "__main__":
    main(sys.argv[1:])
