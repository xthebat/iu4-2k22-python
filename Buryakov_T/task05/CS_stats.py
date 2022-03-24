from dataclasses import dataclass
from typing import List


@dataclass
class Kill:
    attacker_steam_id: int
    attacker_name: str
    attacker_team: str
    victim_steam_id: int
    victim_name: str
    victim_team: str
    assister_steam_id: int
    assister_name: str
    assister_team: str

    @classmethod
    def from_data(cls, data: dict) -> "Kill":
        return Kill(
            attacker_steam_id=data["attackerSteamID"],
            attacker_name=data["attackerName"],
            attacker_team=data["attackerTeam"],
            victim_steam_id=data["victimSteamID"],
            victim_name=data["victimName"],
            victim_team=data["victimTeam"],
            assister_steam_id=data["assisterSteamId"],
            assister_name=data["assisterName"],
            assister_team=data["assisterTeam"]
        )


@dataclass
class Damage:
    attacker_steam_id: int
    attacker_name: str
    victim_steam_id: int
    victim_name: str
    weapon: str
    hp_damage_taken: int
    hit_group: str
    is_friendly_fire: bool
    distance: float


@dataclass
class Player:
    steam_id: int
    name: str
    team: str
    player_side: str


@dataclass
class Round:
    num: int
    is_warmup: bool
    t_score: int
    ct_score: int
    winning_side: str
    winning_team: str
    losing_team: str
    kills: list[Kill]

    @classmethod
    def from_data(cls, data: dict) -> "Round":
        kills_data = [Kill.from_data(it) for it in data["kills"]]
        return Round(
            num=data["roundNum"],
            is_warmup=data["isWarmup"],
            t_score=data["tScore"],
            ct_score=data["ctScore"],
            winning_side=data["winningSide"],
            winning_team=data["winningTeam"],
            losing_team=data["losingTeam"],
            kills=kills_data
        )


def _get_start_index(rounds: List[Round]):
    for index, game_round in enumerate(reversed(rounds)):
        if game_round.t_score == 0 and game_round.ct_score == 0:
            return len(rounds) - index - 1
    raise IndexError("Can't find valid start found")


def _fix_rounds_in_place(rounds: List[Round]):
    start_index = _get_start_index(rounds)
    invalid_rounds = rounds[:start_index]
    while invalid_rounds:
        invalid_round = invalid_rounds.pop()
        rounds.remove(invalid_round)
    for it in rounds:
        if it.winning_team is None:
            rounds.remove(it)
        it.num -= start_index


def _fix_rounds(rounds: List[Round]):
    start_index = _get_start_index(rounds)
    start_number = rounds[start_index].num - 1
    result = rounds[start_index:]
    for it in result:
        it.num -= start_number
    return list(it for it in result if it.winning_team is not None)


@dataclass
class Match:
    match_id: str
    map_name: str
    game_rounds: List[Round]

    @classmethod
    def from_data(cls, data: dict, fix_rounds: bool = True) -> "Match":
        game_rounds = [Round.from_data(it) for it in data["gameRounds"]]
        return Match(
            match_id=data["matchID"],
            map_name=data["mapName"],
            game_rounds=game_rounds if not fix_rounds else _fix_rounds(game_rounds)
        )

    def print(self):
        print('\n'.join(str(it) for it in self.game_rounds))
