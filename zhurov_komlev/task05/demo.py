from dataclasses import dataclass
from typing import List


class Round_OldStyle:

    def __init__(
            self,
            num: int,
            is_warmup: bool,
            t_score: int,
            ct_score: int,
            winner_team: str,
            winner_side: str,
    ):
        self.num = num
        self.is_warmup = is_warmup
        self.t_score = t_score
        self.ct_score = ct_score
        self.winner_team = winner_team
        self.winner_side = winner_side

    def __str__(self):
        return f"Round(num={self.num},...)"


@dataclass
class Kill:
    attacker_team: str
    attacker_name: str
    attacker_side: str
    victim_team: str
    victim_name: str
    victim_side: str

    @classmethod
    def from_data(cls, data: dict) -> "Kill":
        return Kill(
            attacker_team=data["attackerTeam"],
            attacker_name=data["attackerName"],
            attacker_side=data["attackerSide"],
            victim_team=data["victimTeam"],
            victim_name=data["victimName"],
            victim_side=data["victimSide"],
        )


@dataclass
class Round:
    num: int
    is_warmup: bool
    t_score: int
    ct_score: int
    winner_team: str
    winner_side: str
    kills: List[Kill]

    @classmethod
    def from_data(cls, data: dict) -> "Round":
        kills = [Kill.from_data(it) for it in data["kills"]]
        return Round(
            num=data["roundNum"],
            is_warmup=data["isWarmup"],
            t_score=data["tScore"],
            ct_score=data["ctScore"],
            winner_team=data["winningTeam"],
            winner_side=data["winningSide"],
            kills=kills
        )

    @classmethod
    def from_csv(cls, csv: str) -> "Round":
        raise NotImplemented


def _game_start_index(rounds: List[Round]):
    for index, it in enumerate(reversed(rounds)):
        if it.t_score == 0 and it.ct_score == 0:
            return len(rounds) - index - 1
    raise IndexError("Can't find valid start round")


def _fix_rounds_in_place(rounds: List[Round]):
    start_index = _game_start_index(rounds)
    start_number = rounds[start_index].num - 1
    invalid_rounds = rounds[:start_index]

    while invalid_rounds:
        invalid_round = invalid_rounds.pop()
        rounds.remove(invalid_round)

    for it in rounds:
        it.num -= start_number


def _fix_rounds(rounds: List[Round]) -> List[Round]:
    start_index = _game_start_index(rounds)
    start_number = rounds[start_index].num - 1
    result = rounds[start_index:]
    for it in result:
        it.num -= start_number
    return list(it for it in result if it.winner_team is not None)


@dataclass
class Match:
    match_id: str
    map_name: str
    rounds: List[Round]

    @classmethod
    def from_data(cls, data: dict, fix_rounds: bool = True) -> "Match":
        rounds = [Round.from_data(it) for it in data["gameRounds"]]
        return Match(
            match_id=data["matchID"],
            map_name=data["mapName"],
            rounds=rounds if not fix_rounds else _fix_rounds(rounds)
        )

    def print(self):
        print("\n".join(str(it) for it in self.rounds))
