import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import List, Dict


PROG_NAME = "csgo_stats.py"
STATUS_CONNECT = "connect"


class JsonHandler:

    @staticmethod
    def process_json(json_file: str) -> dict:
        try:
            with open(json_file, "r") as f:
                return json.load(f)
        except ValueError as e:
            print('Invalid JSON: ' + json_file)
            return {}


@dataclass
class PlayerStats:
    kills: int
    deaths: int
    assists: int
    ud: int
    ef: int
    hs: float
    acc: float
    adr: float
    kast: float
    rating2: float

    @classmethod
    def from_data(cls, data: dict, steam_id: int) -> "PlayerStats":
        pass


class Player:

    def __init__(self, nickname: str, team: str, steam_id: int, stats: PlayerStats = None,
                 matchmaking_rank: str = "", status: str = ""):
        self.nickname = nickname
        self.team = team
        self.steam_id = steam_id
        self.stats = stats
        self.matchmaking_rank = matchmaking_rank
        self.status = status


@dataclass
class KillInfo:
    killer: Player
    victim: Player
    timestamp: int
    weapon: str

    @classmethod
    def from_data(cls, data: dict) -> "KillInfo":
        pass


@dataclass
class MatchInfo:
    map: str
    tickrate: int
    rounds: int
    matchtime: int

    @classmethod
    def from_data(cls, data: dict) -> "MatchInfo":
        rounds_count = 0
        matchtime = 0
        return MatchInfo(map=data["mapName"], tickrate=data["tickRate"], rounds=rounds_count, matchtime=matchtime)


@dataclass
class MainStats:
    players: List[Player]
    match: MatchInfo

    @classmethod
    def from_data(cls, data: dict) -> "MainStats":
        id_lst = get_players_list(data)
        for round in data["gameRounds"]:
            pass
        return MainStats(players=id_lst, match=MatchInfo.from_data(data))

    def generate_output(self) -> str:
        pass

    def __str__(self):
        return self.generate_output()


@dataclass
class RoundStats:
    kills: List[KillInfo]

    @classmethod
    def from_data(cls, data: dict) -> "RoundStats":
        return RoundStats(kills=list())

    def generate_output(self) -> str:
        pass

    def __str__(self):
        return self.generate_output()


def get_players_list(data: dict) -> list:
    unique_ids = set()
    players_lst = list()
    for connection in data["playerConnections"]:
        action = connection["action"]
        steam_id = connection["steamID"]
        if action == STATUS_CONNECT and steam_id and steam_id not in unique_ids:
            unique_ids.add(steam_id)
            players_lst.append(steam_id)
    return players_lst


def main(args: List[str]):
    # get arguments
    prog_idx = args.index(PROG_NAME)
    args = args[prog_idx + 1:]
    # create parser
    parser = argparse.ArgumentParser(prog=PROG_NAME, description="Console utility for analysis CSGO .dem file "
                                                                 "from preselected .json representation")
    parser.add_argument("path", help="path to csgo .json file", type=argparse.FileType('r'))
    parser.add_argument("-r", "--round", help="round number", type=int)
    parsed_args = parser.parse_args(args)
    json_data = JsonHandler.process_json(parsed_args.path.name)
    if len(json_data):
        if parsed_args.round:
            stats = RoundStats.from_data(json_data)
            print(stats.generate_output())
        else:
            stats = MainStats.from_data(json_data)
            print(stats.generate_output())


if __name__ == '__main__':
    main(sys.argv)
