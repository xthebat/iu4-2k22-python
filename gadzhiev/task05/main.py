import json
import sys
from demo import *


def main(args: list):
    with open(args[1], "rt") as file:
        text = file.read()
        data = json.loads(text)
    print(data)

    match = GameMatch.from_data(data)
    match.print()


if __name__ == '__main__':
    main(sys.argv)
