import sys
import json
from dataclasses import dataclass


@dataclass
class RoundResult:
    ct_win: bool = None
    t_win: bool = None

    def __bool__(self):
        if ct_win:
            return True
        elif t_win:
            return False
        else:
            return None

    def __str__(self):
        if ct_win:
            return "CounterTerroristsWin"
        elif t_win:
            return "TerroristsWin"


class Game:
    id: str
    map: str

    def __init__(self):
        self.rounds = list()
        self.ct_players = list()
        self.t_players = list()

    def parse(self, file_name: str):
        with open(file_name, "rt") as file:
            text = file.read()
            data = json.loads(text)
        self.id = data["matchID"]
        self.map = data["mapName"]

        for data_round in data["gameRounds"]:
            cs_round = Round(self)
            cs_round.parse(data_round)
            self.rounds.append(cs_round)

    def add_player(self, player: "Player"):
        if player.side == "CT":
            self.ct_players.append(player)
        elif player.side == "T":
            self.t_players.append(player)

    def get_player(self, player_name: str) -> "Player":
        for player in self.ct_players:
            if player.name == player_name:
                return player
        for player in self.t_players:
            if player.name == player_name:
                return player
        return None


class Round:

    def __init__(self, game: "Game"):
        self.result = RoundResult()
        self.game = game

    def parse(self, data_round):
        if data_round["winningSide"] == "CT":
            self.result = RoundResult(ct_win=True)
        elif data_round["winningSide"] == "T":
            self.result = RoundResult(t_win=True)

        self.__kill_parser(data_round)
        self.__damage_parser(data_round)
        self.__fires_parser(data_round)

    def __kill_parser(self, data_round):
        for data_kill in data_round["kills"]:
            attacker = self.game.get_player(data_kill["attackerName"])
            victim = self.game.get_player(data_kill["victimName"])
            assister = self.game.get_player(data_kill["assisterName"])
            if attacker is None:
                attacker = Player(data_kill["attackerName"], data_kill["attackerTeam"], data_kill["attackerSide"])
                self.game.add_player(attacker)
            if victim is None:
                victim = Player(data_kill["victimName"], data_kill["victimTeam"], data_kill["victimSide"])
                self.game.add_player(victim)
            if assister is None:
                assister = Player(data_kill["assisterName"], data_kill["assisterTeam"], data_kill["assisterSide"])
                self.game.add_player(assister)

            attacker.kills += 1
            victim.deaths += 1
            assister.assists += 1

            if data_kill["isTrade"] and data_kill["playerTradedName"] == attacker.name:
                attacker.trades += 1
            elif data_kill["isTrade"] and data_kill["playerTradedName"] == victim.name:
                victim.trades += 1
            if data_kill["isHeadshot"]:
                attacker.headshots += 1

    def __damage_parser(self, data_round):
        for data_damage in data_round["damages"]:
            attacker = self.game.get_player(data_damage["attackerName"])
            if attacker is None:
                attacker = Player(data_damage["attackerName"], data_damage["attackerTeam"], data_damage["attackerSide"])
                self.game.add_player(attacker)

            attacker.total_damage += data_damage["hpDamageTaken"]
            if data_damage["weapon"] == "HE Grenade" or data_damage["weapon"] == "Molotv":  # он там так называется?
                attacker.utility_damage += data_damage["hpDamageTaken"]
            attacker.shots_done += 1

    def __fires_parser(self, data_round):
        for data_fire in data_round["weaponFires"]:
            shooter = self.game.get_player(data_fire["playerName"])
            if shooter is None:
                shooter = Player(data_fire["playerName"], data_fire["playerTeam"], data_fire["playerSide"])
                self.game.add_player(shooter)

            if "Grenade" not in data_fire["weapon"]:
                shooter.shots_missed += 1


@dataclass
class Player:
    name: str
    team: str
    side: str
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    survives: int = 0
    trades: int = 0
    shots_done: int = 0
    shots_missed: int = 0
    headshots: int = 0
    total_damage: int = 0
    utility_damage: int = 0


def main(args):
    if len(args) < 2:
        sys.exit(-1)

    file_name = args[1]

    game = Game()
    game.parse(file_name)


if __name__ == '__main__':
    main(sys.argv)
