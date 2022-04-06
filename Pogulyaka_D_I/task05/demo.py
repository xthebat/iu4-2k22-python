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
    assister_side: str
    is_headshot: bool

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
            assister_side=data["assisterSide"],
            is_headshot=data["isHeadshot"]
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
class Grenade:
    thrower_steam_id: int
    thrower_name: str
    thrower_team: str
    grenade_type: str

    @classmethod
    def from_data(cls, data: dict) -> "Grenade":
        return Grenade(
            thrower_steam_id=data["throwerSteamID"],
            thrower_name=data["throwerName"],
            thrower_team=data["throwerTeam"],
            grenade_type=data["grenadeType"]
        )


@dataclass
class Bomb:
    player_name: str
    bomb_action: str
    player_x: float
    player_y: float
    player_z: float

    @classmethod
    def from_data(cls, data: dict) -> "Bomb":
        return Bomb(
            player_name=data["playerName"],
            bomb_action=data["bombAction"],
            player_x=data["playerX"],
            player_y=data["playerY"],
            player_z=data["playerZ"]
        )


@dataclass
class Round:
    num: int
    is_warmup: bool
    t_score: int
    ct_score: int
    winner_team: str
    winner_side: str
    end_reason: str
    kills: List[Kill]
    damages: List[Damage]
    weapon_fires: List[WeaponFire]
    grenades: List[Grenade]
    bomb_events: List[Bomb]

    @classmethod
    def from_data(cls, data: dict) -> "Round":
        kills = [Kill.from_data(it) for it in data["kills"]]
        damages = [Damage.from_data(it) for it in data["damages"]]
        weapon_fires = [WeaponFire.from_data(it) for it in data["weaponFires"]]
        grenades = [Grenade.from_data(it) for it in data["grenades"]]
        bombs = [Bomb.from_data(it) for it in data["bombEvents"]]
        return Round(
            num=data["roundNum"],
            is_warmup=data["isWarmup"],
            t_score=data["tScore"],
            ct_score=data["ctScore"],
            winner_team=data["winningTeam"],
            winner_side=data["winningSide"],
            end_reason=data["roundEndReason"],
            kills=kills,
            damages=damages,
            weapon_fires=weapon_fires,
            grenades=grenades,
            bomb_events=bombs
        )


def _get_players_nicknames(data: dict):
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


def _get_player_team(rounds: List[Round], name: str):
    for round in rounds:
        kills = round.kills
        for kill in kills:
            if kill.attacker_name == name:
                return kill.attacker_team
            if kill.victim_name == name:
                return kill.victim_team
    raise ValueError("Player's team was not found!")


def _count_player_kills_deaths_assists(rounds: List[Round], name: str):
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


def _get_player_adr(rounds: List[Round], name: str):
    damage_sum = 0
    for round in rounds:
        damages = round.damages
        for damage in damages:
            if damage.attacker_name == name:
                damage_sum += damage.hp_damage
    if damage_sum == 0:
        return 0
    else:
        return damage_sum / len(rounds)


def _get_player_acc(rounds: List[Round], name: str):
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
        return hits / fires


def _get_player_hs(rounds: List[Round], name: str):
    kills = 0
    hs = 0
    for round in rounds:
        for kill in round.kills:
            if name == kill.attacker_name:
                kills += 1
                if kill.is_headshot:
                    hs += 1
    return hs/kills


def _is_loser_team_eliminated(round: Round, winner_side: str) -> bool:
    kill_count = 0
    for kill in round.kills:
        if kill.attacker_side == winner_side and kill.victim_side != winner_side:
            kill_count += 1
    if kill_count == 5:
        return True
    else:
        return False


def _calculate_impacts(rounds: List["Round"], name: str) -> List[int]:
    results = []
    for round in rounds:
        result = 0
        winner_side = round.winner_side
        end_reason = round.end_reason
        for kill in round.kills:
            if name == kill.attacker_name:
                if kill.victim_side != kill.attacker_side:
                    result += 2
                else:
                    result -= 2
            if name == kill.assister_name and kill.assister_side != kill.victim_side:
                result += 1
        for bomb_event in round.bomb_events:
            if name == bomb_event.player_name:
                if bomb_event.bomb_action == "plant":
                    result += 2
                    if end_reason == "TargetBombed":
                        result += 2
                if bomb_event.bomb_action == "defuse":
                    result += 2
                    if _is_loser_team_eliminated(round, winner_side):
                        result += 2
        results.append(result)
    return results


@dataclass
class Player:
    name: str
    team: str
    kills: int
    deaths: int
    assists: int
    adr: float
    acc: float
    hs: float
    impacts: list[int]

    @classmethod
    def from_data(cls, name: str, rounds: List[Round]) -> "Player":
        team = _get_player_team(rounds, name)
        kills_deaths_assists = _count_player_kills_deaths_assists(rounds, name)
        adr = _get_player_adr(rounds, name)
        acc = _get_player_acc(rounds, name)
        hs = _get_player_hs(rounds, name)
        impacts = _calculate_impacts(rounds, name)
        return Player(
            name=name,
            team=team,
            kills=kills_deaths_assists[0],
            deaths=kills_deaths_assists[1],
            assists=kills_deaths_assists[2],
            adr=adr,
            acc=acc,
            hs=hs,
            impacts=impacts
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


def _formatted_output(title, str_value) -> "str":
    spaces_front = (len(title) - len(str(str_value))) // 2
    spaces_back = len(title) - len(str(str_value)) - spaces_front
    return spaces_front*' ' + str(str_value) + spaces_back*' ' + '|'


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
        nicknames = _get_players_nicknames(data)
        players = [Player.from_data(it, _fix_rounds(rounds)) for it in nicknames]
        return Match(
            match_id=data["matchID"],
            map_name=data["mapName"],
            rounds=rounds if not fix_rounds else _fix_rounds(rounds),
            players=players
        )

    def players_print(self):
        team = "       Team       "
        name = "     Name     "
        kills = " Kills "
        deaths = " Deaths "
        assists = " Assists "
        adr = "   ADR   "
        accuracy = " Accuracy "
        hs = "   HS   "
        score = " Score "
        print(team, name, kills, deaths, assists, adr, accuracy, hs, score, '', sep='|')
        for player in self.players:
            print(_formatted_output(team, player.team), end='')
            print(_formatted_output(name, player.name), end='')
            print(_formatted_output(kills, player.kills), end='')
            print(_formatted_output(deaths, player.deaths), end='')
            print(_formatted_output(assists, player.assists), end='')
            print(_formatted_output(adr, round(player.adr, 3)), end='')
            print(_formatted_output(accuracy, round(player.acc, 3)), end='')
            print(_formatted_output(hs, round(player.hs, 3)), end='')
            print(_formatted_output(score, sum(player.impacts)))

    def match_print(self):
        num = "   №   "
        t_score = "   T   "
        ct_score = "   CT   "
        win_team = "     Winner team     "
        kills = "   Kills   "
        end_reason = "       Result       "
        print(num, t_score, ct_score, win_team, kills, end_reason, '', sep='|')
        for round in self.rounds:
            print(_formatted_output(num, round.num), end='')
            print(_formatted_output(t_score, round.t_score), end='')
            print(_formatted_output(ct_score, round.ct_score), end='')
            print(_formatted_output(win_team, round.winner_team), end='')
            print(_formatted_output(kills, len(round.kills)), end='')
            print(_formatted_output(end_reason, round.end_reason))
