import json
import os
from typing import Iterable, List

from thebat.sem06.demo import Round, Match, MatchEncapsulated
from thebat.sem06.parsers import FileInterface, CommonFile

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


def read_data(file: FileInterface, address, size: int):
    file.open(address)
    data = file.read(size)
    return data


def main():
    with open("temp/1-266bdc4c-3672-4cd5-bc97-b79c6c1e4d6a-1-1.json", "rt") as file:
        text = file.read()
        data = json.loads(text)

    nicknames = get_players_nicknames(data)

    match = Match.from_data(data)

    match_enc1 = MatchEncapsulated.from_data(data)
    match_enc2 = MatchEncapsulated.from_data(data)

    match_enc2.reset("11")

    file = CommonFile()
    read_data(file, "temp/1-266bdc4c-3672-4cd5-bc97-b79c6c1e4d6a-1-1.json", 1024)

    print(match_enc1.match_id)
    # match_enc.match_id = "111"
    # match_enc1.get_round_by_num(1)

    # matrix[1, 2, 3] * matrix[5, :, :]
    # matrix.get_value_by_index(1, 2, 3).multiply_by_column(matrix.get_column(5))

    print(match_enc1[1])
    print([match_enc1])
    print(match_enc1)

    for rnd in match_enc1:
        print(rnd)

    for player in match_enc1.players:
        print(player)

    print(match_enc1 == match_enc2)
    print(match_enc1 != match_enc2)

    # table1.select(table1.name == "20").do_request()

    # for round in match.rounds:
    #     pass

    # match.print()

    match_enc1.reset("111")


if __name__ == '__main__':
    main()
