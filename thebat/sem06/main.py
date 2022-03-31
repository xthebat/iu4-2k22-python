import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from thebat.sem06.demo import Round, Match, MatchEncapsulated
from thebat.sem06.interface_example import FileInterface, CommonFile
from thebat.sem06.parsers import ParserRegistry, JsonDemoParser, DemDemoParser, GzDemoParser, Frames

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


def sem07():
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


STATE = 0


def func_with_state(x):
    global STATE
    STATE += x
    return STATE


def clear_func(x, y):
    return x + y


def sem08():
    registry = ParserRegistry()\
        .register(".json", JsonDemoParser)\
        .register(".dem", DemDemoParser)\
        .register(".gz", GzDemoParser)

    demo = registry.parse("temp/003539831729474764830_0420161581.dem", parse_rate=1)
    frames = Frames.from_demo(demo).dump("temp/003539831729474764830_0420161581.zip")

    # print(frames)

    # for file in Path("temp").iterdir():
    #     demo = registry.parse_or_none(str(file))
    #     if demo is not None:
    #         print(f"{file} parse ok")


if __name__ == '__main__':
    sem08()
