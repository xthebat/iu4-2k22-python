from dataclasses import dataclass
from typing import List, Iterable

INVALID_STEAM_ID = 0
FLOAT_AVERAGING = 2


@dataclass
class WeaponFire:
    player_team: str
    player_name: str
    weapon: str

    @classmethod
    def from_data(cls, data: dict) -> "WeaponFire":
        return WeaponFire(
            player_name=data["playerName"],
            player_team=data["playerTeam"],
            weapon=data["weapon"]
        )


@dataclass
class Kill:
    attacker_team: str
    attacker_name: str
    attacker_side: str
    victim_team: str
    victim_name: str
    victim_side: str
    assister_name: str
    suicide: bool
    headshot: bool
    is_trade: bool
    player_traded_name: str

    @classmethod
    def from_data(cls, data: dict) -> "Kill":
        return Kill(
            attacker_team=data["attackerTeam"],
            attacker_name=data["attackerName"],
            attacker_side=data["attackerSide"],
            victim_team=data["victimTeam"],
            victim_name=data["victimName"],
            victim_side=data["victimSide"],
            assister_name=data["assisterName"],
            suicide=data["isSuicide"],
            headshot=data["isHeadshot"],
            is_trade=data["isTrade"],
            player_traded_name=data["playerTradedName"],
        )


@dataclass
class Damage:
    friendly_fire: bool
    hp_damage_taken: int
    weapon: str
    attacker_name: str
    victim_name: str

    @classmethod
    def from_data(cls, data: dict) -> "Damage":
        return Damage(
            attacker_name=data["attackerName"],
            victim_name=data["victimName"],
            weapon=data["weapon"],
            hp_damage_taken=data["hpDamageTaken"],
            friendly_fire=data["isFriendlyFire"]
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


@dataclass
class Player:
    name: str
    kills: int
    deaths: int
    assists: int
    acc: float
    hs: float
    adr: float
    ud: int
    kast: float
    # rat2_0: float
    team: str

    @classmethod
    def from_data(cls, name: str, rounds: List[Round]) -> "Player":
        kda = get_player_kda(rounds, name)
        team = get_player_team(rounds, name)
        acc = get_player_acc(rounds, name)
        hs = get_player_hs(rounds, name, kda[0])
        adr = get_player_adr(rounds, name)
        ud = get_player_ud(rounds, name)
        kast = get_player_kast(rounds, name)
        # rat2_0 = get_player_rat2_0(rounds, name)
        return Player(
            name=name,
            team=team,
            acc=acc,
            hs=hs,
            adr=adr,
            ud=ud,
            kast=kast,
            # rat2_0=rat2_0,
            kills=kda[0],
            deaths=kda[1],
            assists=kda[2]
        )


@dataclass
class Match:
    match_id: str
    map_name: str
    rounds: List[Round]
    players: List[Player]

    @classmethod
    def from_data(cls, data: dict, fix_rounds: bool = True) -> "Match":
        rounds = [Round.from_data(it) for it in data["gameRounds"]]
        nicknames = get_players_nicknames(data)
        rounds = _fix_rounds(rounds)
        players = [Player.from_data(it, _fix_rounds(rounds)) for it in nicknames]
        return Match(
            match_id=data["matchID"],
            map_name=data["mapName"],
            rounds=rounds if not fix_rounds else _fix_rounds(rounds),
            players=players
        )

    def players_print(self):
        print("\n".join(str(it) for it in self.players))


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
    raise ValueError("Player can't be here!")


def get_player_team(rounds: List[Round], name: str):
    for num_round in rounds:
        kills = num_round.kills
        for kill in kills:
            if kill.attacker_name == name:
                return kill.attacker_team
            if kill.victim_name == name:
                return kill.victim_team
    raise ValueError("Team can't be here")


def _game_start_index(rounds: List[Round]):
    for index, it in enumerate(reversed(rounds)):
        if it.t_score == 0 and it.ct_score == 0:
            return len(rounds) - index - 1
    raise IndexError("Can't find valid start round")


def _fix_rounds(rounds: List[Round]) -> List[Round]:
    start_index = _game_start_index(rounds)
    start_number = rounds[start_index].num - 1
    result = rounds[start_index:]
    for it in result:
        it.num -= start_number
    return list(it for it in result if it.winner_team is not None)


def get_player_acc(rounds: List[Round], name: str):
    shoots = 0
    hits = 0
    for num_round in rounds:
        damages = num_round.damages
        for damage in damages:
            if damage.attacker_name == name:
                hits += 1
        for shoot in num_round.weapon_fires:
            if shoot.player_name == name and shoot.weapon.find('grenade') == -1:
                shoots += 1
    if shoots:
        return round(shoots/hits, FLOAT_AVERAGING)
    else:
        return 0


def get_player_kda(rounds: List[Round], name: str) -> list:
    kda = [0, 0, 0]
    for num_round in rounds:
        kills = num_round.kills
        for kill in kills:
            if kill.suicide and kill.attacker_name == name:
                kda[0] -= 1
                kda[1] += 1
            elif kill.attacker_name == name:
                kda[0] += 1
            elif kill.victim_name == name:
                kda[1] += 1
            if kill.assister_name == name:
                kda[2] += 1
    return kda


def get_player_hs(rounds: List[Round], name: str, death: int) -> float:
    if death == 0:
        return 0

    hs_count = 0
    for num_round in rounds:
        kills = num_round.kills
        for kill in kills:
            if kill.attacker_name == name and kill.headshot:
                hs_count += 1
    return round(hs_count/death, FLOAT_AVERAGING)


def get_player_adr(rounds: List[Round], name: str) -> float:
    damage_count = 0
    rounds_count = len(rounds)
    for num_round in rounds:
        damages = num_round.damages
        for damage in damages:
            if damage.attacker_name == name:
                damage_count += damage.hp_damage_taken
    return round(damage_count/rounds_count, FLOAT_AVERAGING)


def get_player_ud(rounds: List[Round], name: str) -> int:
    damage_count = 0
    for num_round in rounds:
        damages = num_round.damages
        for damage in damages:
            if damage.attacker_name == name and damage.weapon == "HE Grenade":
                damage_count += damage.hp_damage_taken
    return damage_count


# процент от раундов, когда игрок сделал убийство, ассист или выжил,
# а также случаи когда его разменяли сразу после смерти
def get_player_kast(rounds: List[Round], name: str) -> float:
    kast_count = 0
    rounds_count = len(rounds)
    for num_round in rounds:
        useful = False    # kill or assist
        survive = True
        trade_after_death = False

        kills = num_round.kills
        for kill in kills:
            if kill.attacker_name == name or kill.assister_name == name:
                useful = True
            elif kill.victim_name == name:
                survive = False
            elif kill.player_traded_name == name:
                trade_after_death = True

        if useful or survive or (trade_after_death and not survive):
            kast_count += 1

    return round(kast_count/rounds_count, FLOAT_AVERAGING)


# Статья с формулой рейтинга 2.0
# https://escorenews.com/ru/csgo/news/14681-fanat-cs-go-nashel-formulu-reytinga-2-0-ot-hltv-teper-vy-mojete-poschitat-svoy-sobstvennyj
# RAT2_0 = 0.0073 * KAST + 0.3591 * KPR - 0.5329 * DPR + 0.2372 * Impact + 0.0032 * ADR + 0.1587
# Impact = 2.13 * KPR + 0.32 * (Assists per round) -0.41
# def get_player_rat2_0(rounds: List[Round], name: str):
#       0.0073 * KAST \
#     + 0.3591 * KPR \
#     - 0.5329 * DPR \
#     + 0.2372 * Impact \
#     + 0.0032 * ADR \
#     + 0.1587
#
#     name = name,
#     team = team,
#     acc = acc,
#     # hs=hs,
#     # adr=adr,
#     # ud=ud,
#     # kast=kast,
#     rat2_0 = rat2_0,
#     kills = kda[0],
#     deaths = kda[1],
#     assists = kda[2]

