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


class MatchEncapsulated:

    def __init__(self, match_id: str, map_name: str, rounds: List[Round] = None):
        self.__match_id = match_id
        self.__map_name = map_name
        self.__rounds = rounds or list()

    @classmethod
    def from_data(cls, data: dict, fix_rounds: bool = True) -> "MatchEncapsulated":
        rounds = [Round.from_data(it) for it in data["gameRounds"]]
        return MatchEncapsulated(
            match_id=data["matchID"],
            map_name=data["mapName"],
            rounds=rounds if not fix_rounds else _fix_rounds(rounds)
        )

    @property
    def map_name(self):
        return self.__map_name

    @property
    def match_id(self):
        return self.__match_id

    @property
    def players(self):
        for r in self.__rounds:
            # ...
            yield "player"

    # Anti-pattern
    # @match_id.setter
    # def match_id(self, value):
    #     self.__map_name = None
    #     self.__rounds = list()
    #     self.__match_id = value

    def __getitem__(self, item: int):   # []
        return self.__rounds[item - 1]

    def __str__(self):  # str()
        return f"Match(id={self.__match_id}, map={self.__map_name})"

    def __repr__(self):  # repr()
        return f"Match({self.__match_id})"

    def __iter__(self):  # in
        return self.__rounds.__iter__()

    # def __iter__(self):  # in
    #     return (it for it in self.__rounds)

    # def __iter__(self):  # in
    #     for it in self.__rounds:
    #         yield it

    def __eq__(self, other):
        if not isinstance(other, MatchEncapsulated):
            return False
        return self.__match_id == other.__match_id

    # def __ne__(self, other):
    #     return "I don't know how to compare matches"

    def print(self):
        print("\n".join(str(it) for it in self.__rounds))

    def reset(self, match_id: str):
        self.__match_id = match_id
        self.__map_name = None
        self.__rounds = list()


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
