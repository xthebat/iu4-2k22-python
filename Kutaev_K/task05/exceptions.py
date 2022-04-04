from dataclasses import dataclass


@dataclass
class TeamError(Exception):
    ct_team: str


@dataclass
class GoodRoundsError(Exception):
    pass


@dataclass
class MatchTypeError(Exception):
    max_rounds: int


@dataclass
class PlayersError(Exception):
    pass


@dataclass
class PlayersSteamIDError(Exception):
    players_steam_ids: list
