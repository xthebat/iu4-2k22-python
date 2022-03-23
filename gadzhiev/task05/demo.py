from dataclasses import dataclass
from typing import List


@dataclass
class Kill:
    attacker_team: str
    attacker_name: str
    attacker_side: str
    victim_team: str
    victim_name: str
    victim_side: str
    assister_name: str

    @classmethod
    def from_data(cls, data: dict) -> "Kill":
        return Kill(
            attacker_team=data["attackerTeam"],
            attacker_name=data["attackerName"],
            attacker_side=data["attackerSide"],
            victim_team=data["victimTeam"],
            victim_name=data["victimName"],
            victim_side=data["victimSide"],
            assister_name=data["assisterName"]
        )


@dataclass
class Damage:
    attacker_team: str
    attacker_name: str
    attacker_side: str
    attacker_weapon: str
    victim_team: str
    victim_name: str
    victim_side: str
    hp_damage: int
    is_friendly_fire: bool

    @classmethod
    def from_data(cls, data: dict) -> "Damage":
        return Damage(
            attacker_team=data["attackerTeam"],
            attacker_name=data["attackerName"],
            attacker_side=data["attackerSide"],
            attacker_weapon=data["weapon"],
            victim_team=data["victimTeam"],
            victim_name=data["victimName"],
            victim_side=data["victimSide"],
            hp_damage=data["hpDamageTaken"],
            is_friendly_fire=data["isFriendlyFire"]
        )


@dataclass
class WeaponFire:
    player_team: str
    player_name: str
    player_side: str
    player_weapon: str

    @classmethod
    def from_data(cls, data: dict) -> "WeaponFire":
        return WeaponFire(
            player_team=data["playerTeam"],
            player_name=data["playerName"],
            player_side=data["playerSide"],
            player_weapon=data["weapon"],
        )


@dataclass
class GameRound:
    id: int
    is_warmup: bool
    t_score: int
    ct_score: int
    winning_team: str
    winning_side: str
    kills: List[Kill]
    damages: List[Damage]
    weapon_fires: List[WeaponFire]

    @classmethod
    def from_data(cls, data: dict) -> "GameRound":
        kills = [Kill.from_data(it) for it in data["kills"]]
        damages = [Damage.from_data(it) for it in data["damages"]]
        weapon_fires = [WeaponFire.from_data(it) for it in data["weaponFires"]]
        return GameRound(
            id=data["roundNum"],
            is_warmup=data["isWarmup"],
            t_score=data["tScore"],
            ct_score=data["ctScore"],
            winning_team=data["winningTeam"],
            winning_side=data["winningSide"],
            kills=kills,
            damages=damages,
            weapon_fires=weapon_fires
        )


@dataclass
class Player:
    steam_id: int
    player_name: str
    player_kills: int
    player_death: int
    player_assists: int
    player_accuracy: float
    player_headshots: float
    player_average_damage: float
    player_utility_damage: int
    player_KAST: float
    player_rating_2: float
    rounds: List[GameRound]


@dataclass
class GameMatch:
    id: int
    map_name: str
    rounds: List[GameRound]
    # players: List[Player]

    @classmethod
    def from_data(cls, data: dict) -> "GameMatch":
        rounds = [GameRound.from_data(it) for it in data["gameRounds"]]
        return GameMatch(
            id=data["matchID"],
            map_name=data["mapName"],
            rounds=rounds
        )

    def print(self):
        print("\n".join(str(it) for it in self.rounds))
