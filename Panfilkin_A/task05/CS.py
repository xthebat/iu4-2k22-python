
from typing import List


class Team:
    def __init__(self, name: str, players: List["Player"]) -> None:
        self.name = name
        self.players = players


class Round:
    def __init__(self, round_type: str, round_num: int, kills: List["KillAction"], damages: List["DamageAction"], grenades: List["GrenadeAction"], winning_team: str) -> None:
        self.type = round_type
        self.round_num = round_num
        self.kills = kills
        self.damage = damages
        self.grenade = grenades
        self.winning_team = winning_team


class Match:
    def __init__(self, match_id: str, map_name: str, teams: List["Team"], rounds: List["Round"]) -> None:
        self.match_id = match_id
        self.map_name = map_name
        self.teams = teams
        self.rounds = rounds


class Player:
    def __init__(self, steam_id: str, name: str) -> None:
        self.steam_id = steam_id
        self.name = name
    
    def __str__(self) -> str:
        return f'{self.name}'

class KillAction:
    def __init__(self, attacker: Player, victim: Player, assister: Player, is_suicide: bool, is_teamkill: bool, is_headshot: bool) -> None:
        self.attacker = attacker
        self.victim = victim
        self.assister = assister
        self.is_suicide = is_suicide
        self.is_teamkill = is_teamkill
        self.is_headshot = is_headshot

class DamageAction:
    def __init__(self, attacker: Player, victim: Player, hp_damage_taken: int, is_frendly_fire: bool) -> None:
        self.attacker = attacker
        self.victim = victim
        self.hp_damage_taken = hp_damage_taken
        self.is_frendly_fire = is_frendly_fire

class GrenadeAction:
    def __init__(self, thrower: Player, grenade_type: str) -> None:
        self.thrower = thrower
        self.grenade_type = grenade_type