import json
import os
from typing import Iterable, List

from thebat.sem06.demo import Round, Match

INVALID_STEAM_ID = 0


def get_players_nicknames(data: dict):
    steam_ids = set()
    player_connections = data["playerConnections"]
    for player_connection in player_connections:
        steam_id = player_connection["steamID"]
        if steam_id != INVALID_STEAM_ID:
            steam_ids.add(steam_id)

    player_count = len(steam_ids)

    nicknames = set()
    game_rounds = data["gameRounds"]
    for game_round in game_rounds:
        kills = game_round["kills"]
        for kill in kills:
            attacker = kill["attackerName"]
            victim = kill["victimName"]
            nicknames.add(attacker)
            nicknames.add(victim)
            if len(nicknames) == player_count:
                return nicknames

    raise ValueError("Can't be here!")


def main():
    with open("temp/1-266bdc4c-3672-4cd5-bc97-b79c6c1e4d6a-1-1.json", "rt") as file:
        text = file.read()
        data = json.loads(text)

    nicknames = get_players_nicknames(data)

    match = Match.from_data(data)

    match.print()


if __name__ == '__main__':
    main()
