import json
from task05.exceptions import *
from task05.my_classes import Match
import sys


def main(log_file: str):
    with open(log_file, "rt") as file:
        json_data = file.read()
        data = json.loads(json_data)
    try:
        match: Match = Match.data_to_match(data)
    except GoodRoundsError:
        sys.exit("Wrong input data!\n"
                 "Match does not contains not warm-up rounds")
    except TeamError as error:
        sys.exit("Wrong input data!\n"
                 f"Team '{error}' does not found in game statistics")
    except PlayersError:
        sys.exit("Wrong input data!\n"
                 "Match does not contains enough players\n")
    except PlayersSteamIDError as error:
        sys.exit("Wrong input data!\n"
                 f"Player with Steam ID {error} does not found in game statistics")
    print(match)

    return 0


if __name__ == '__main__':
    main("1-bc6f4da7-e96b-4070-9a66-6392718d3ba6-1-1.json")  # 5 x 5
    main("1-266bdc4c-3672-4cd5-bc97-b79c6c1e4d6a-1-1.json")  # 2 x 2
