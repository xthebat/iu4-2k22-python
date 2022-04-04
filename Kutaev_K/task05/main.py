import json
import sys
from task05.exceptions import *
from task05.my_classes import Match, Statistics
from prettytable import PrettyTable


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

    stats: Statistics = Statistics.calculate_stats(match)

    print(f"Match №'{match.id}' Map: {match.map}\n"
          f"{stats.team_a.name} VS {stats.team_b.name}\n"
          f"First Half:    {stats.team_a.first_half_score}:{stats.team_b.first_half_score}\n"
          f"Second Half:   {stats.team_a.second_half_score}:{stats.team_b.second_half_score}\n"
          f"Final score:   {stats.team_a.final_score}:{stats.team_b.final_score}")

    index: int = 1
    table = PrettyTable(["№", "Player", "K", "D", "A", "ACC%", "HS%", "ADR", "UD", "KAST%"])
    for team in stats:
        for player_stats in team.player_stats:
            table.add_row([index,
                           player_stats.name,
                           player_stats.kills_count,
                           player_stats.deaths_count,
                           player_stats.assist_count,
                           player_stats.accuracy,
                           player_stats.hs_percent,
                           player_stats.average_round_damage,
                           player_stats.utility_damage,
                           player_stats.kast])
            index += 1
    print(table)
    return 0


if __name__ == '__main__':
    main("1-bc6f4da7-e96b-4070-9a66-6392718d3ba6-1-1.json")  # 5 x 5
    main("1-266bdc4c-3672-4cd5-bc97-b79c6c1e4d6a-1-1.json")  # 2 x 2
