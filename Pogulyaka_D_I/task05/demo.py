from dataclasses import dataclass
from typing import List, Iterable


INVALID_STEAM_ID = 0


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
    victim_team: str
    victim_name: str
    weapon: str
    hp_damage: int
    is_friendly_fire: bool

    @classmethod
    def from_data(cls, data: dict) -> "Damage":
        return Damage(
            attacker_team=data["attackerTeam"],
            attacker_name=data["attackerName"],
            victim_team=data["victimTeam"],
            victim_name=data["victimName"],
            weapon=data["weapon"],
            hp_damage=data["hpDamage"],
            is_friendly_fire=data["isFriendlyFire"]
        )


@dataclass
class WeaponFire:
    player_team: str
    player_name: str
    weapon: str

    @classmethod
    def from_data(cls, data: dict) -> "WeaponFire":
        return WeaponFire(
            player_team=data["playerTeam"],
            player_name=data["playerName"],
            weapon=data["weapon"]
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
    damages: List[Damage]
    weapon_fires: List[WeaponFire]

    @classmethod
    def from_data(cls, data: dict) -> "Round":
        kills = [Kill.from_data(it) for it in data["kills"]]
        damages = [Damage.from_data(it) for it in data["damages"]]
        weapon_fires = [WeaponFire.from_data(it) for it in data["weaponFires"]]
        return Round(
            num=data["roundNum"],
            is_warmup=data["isWarmup"],
            t_score=data["tScore"],
            ct_score=data["ctScore"],
            winner_team=data["winningTeam"],
            winner_side=data["winningSide"],
            kills=kills,
            damages=damages,
            weapon_fires=weapon_fires
        )


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

    raise ValueError("Not all players were found!")


def get_player_team(rounds: List[Round], name: str):
    for round in rounds:
        kills = round.kills
        for kill in kills:
            if kill.attacker_name == name:
                return kill.attacker_team
            if kill.victim_name == name:
                return kill.victim_team
    raise ValueError("Player's team was not found!")


def count_player_kills_deaths_assists(rounds: List[Round], name: str):
    counter = [0, 0, 0]
    for round in rounds:
        kills = round.kills
        for kill in kills:
            if kill.attacker_name == name:
                counter[0] += 1
            if kill.victim_name == name:
                counter[1] += 1
            if kill.assister_name == name:
                counter[2] += 1
    return counter


def get_player_adr(rounds: List[Round], name: str):
    damage_sum = 0
    for round in rounds:
        damages = round.damages
        for damage in damages:
            if damage.attacker_name == name:
                damage_sum += damage.hp_damage
    if damage_sum == 0:
        return 0
    else:
        return damage_sum/len(rounds)


def get_player_acc(rounds: List[Round], name: str):
    hits = 0
    fires = 0
    for round in rounds:
        damages = round.damages
        for damage in damages:
            if damage.attacker_name == name:
                hits += 1
        for fire in round.weapon_fires:
            if fire.player_name == name and fire.weapon.find('grenade') == -1:
                fires += 1
    if fires == 0:
        return 0
    else:
        return hits/fires


@dataclass
class Player:
    name: str
    team: str
    kills: int
    deaths: int
    assists: int
    adr: float
    acc: float

    @classmethod
    def from_data(cls, name: str, rounds: List[Round]) -> "Player":
        team = get_player_team(rounds, name)
        kills_deaths_assists = count_player_kills_deaths_assists(rounds, name)
        adr = get_player_adr(rounds, name)
        acc = get_player_acc(rounds, name)
        return Player(
            name=name,
            team=team,
            kills=kills_deaths_assists[0],
            deaths=kills_deaths_assists[1],
            assists=kills_deaths_assists[2],
            adr=adr,
            acc=acc
        )


def _get_start_index(rounds: Iterable[Round]):
    for round in reversed(rounds):
        if round.t_score == 0 and round.ct_score == 0:
            return round.num
    raise IndexError("Can't find valid start round!")


def _fix_rounds(rounds: List[Round]) -> List[Round]:
    start_index = _get_start_index(rounds) - 1
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
    players: List[Player]

    @classmethod
    def from_data(cls, data: dict, fix_rounds: bool = True) -> "Match":
        rounds = [Round.from_data(it) for it in data["gameRounds"]]
        rounds = _fix_rounds(rounds)
        nicknames = get_players_nicknames(data)
        players = [Player.from_data(it, _fix_rounds(rounds)) for it in nicknames]
        return Match(
            match_id=data["matchID"],
            map_name=data["mapName"],
            rounds=rounds if not fix_rounds else _fix_rounds(rounds),
            players=players
        )

    def players_print(self):
        print("\n".join(str(it) for it in self.players))

    def match_print(self):
        print("\n".join(str(it) for it in self.rounds))
