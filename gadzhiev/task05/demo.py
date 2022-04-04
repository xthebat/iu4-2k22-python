from dataclasses import dataclass
from typing import List

INVALID_STEAM_ID = 0
GRENADES = ["Molotov", "Smoke Grenade", "HE Grenade", "Incendiary Grenade", "Flashbang", "Decoy Grenade"]
TERRORIST_SIDE = "T"
CONTER_TERRORIST_SIDE = "CT"


@dataclass
class Kill:
    attacker_team: str
    attacker_name: str
    attacker_steam_id: str
    attacker_side: str
    weapon: str
    victim_team: str
    victim_name: str
    victim_steam_id: str
    victim_side: str
    assister_name: str
    is_friendly_fire: bool
    is_headshot: bool
    is_suicide: bool
    is_trade: bool

    @classmethod
    def from_data(cls, data: dict) -> "Kill":
        return Kill(
            attacker_team=data["attackerTeam"],
            attacker_name=data["attackerName"],
            attacker_steam_id=data["attackerSteamID"],
            attacker_side=data["attackerSide"],
            weapon=data["weapon"],
            victim_team=data["victimTeam"],
            victim_name=data["victimName"],
            victim_steam_id=data["victimSteamID"],
            victim_side=data["victimSide"],
            assister_name=data["assisterName"],
            is_friendly_fire=data["isTeamkill"],
            is_headshot=data["isHeadshot"],
            is_suicide=data["isSuicide"],
            is_trade=data["isTrade"]
        )


@dataclass
class Damage:
    attacker_name: str
    attacker_weapon: str
    victim_name: str
    hp_damage: int
    is_friendly_fire: bool

    @classmethod
    def from_data(cls, data: dict) -> "Damage":
        return Damage(
            attacker_name=data["attackerName"],
            attacker_weapon=data["weapon"],
            victim_name=data["victimName"],
            hp_damage=data["hpDamageTaken"],
            is_friendly_fire=data["isFriendlyFire"]
        )


@dataclass
class WeaponFire:
    team: str
    name: str
    side: str
    weapon: str

    @classmethod
    def from_data(cls, data: dict) -> "WeaponFire":
        return WeaponFire(
            team=data["playerTeam"],
            name=data["playerName"],
            side=data["playerSide"],
            weapon=data["weapon"]
        )


@dataclass
class GameRound:
    round_id: int
    is_warmup: bool
    t_score: int
    ct_score: int
    winning_team: str
    winning_side: str
    losing_team: str
    kills: List[Kill]
    damages: List[Damage]
    weapon_fires: List[WeaponFire]

    @classmethod
    def from_data(cls, data: dict) -> "GameRound":
        kills = [Kill.from_data(it) for it in data["kills"]]
        damages = [Damage.from_data(it) for it in data["damages"]]
        weapon_fires = [WeaponFire.from_data(it) for it in data["weaponFires"]]
        return GameRound(
            round_id=data["roundNum"],
            is_warmup=data["isWarmup"],
            t_score=data["tScore"],
            ct_score=data["ctScore"],
            winning_team=data["winningTeam"],
            winning_side=data["winningSide"],
            losing_team=data["losingTeam"],
            kills=kills,
            damages=damages,
            weapon_fires=weapon_fires,
        )


def _game_start_index(rounds: List[GameRound]):
    for index, it in enumerate(reversed(rounds)):
        if it.t_score == 0 and it.ct_score == 0:
            return len(rounds) - index - 1
    raise IndexError("Can't find valid start round")


def _fix_rounds(rounds: List[GameRound]) -> List[GameRound]:
    start_index = _game_start_index(rounds)
    start_number = rounds[start_index].round_id - 1
    result = rounds[start_index:]
    for it in result:
        it.round_id -= start_number
    return list(it for it in result if it.winning_team is not None)


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
                return list(nicknames)
    raise ValueError("Can't be here!")


def _get_steam_id(name: str, rounds: List[GameRound]) -> str:
    for game_round in rounds:
        for kill in game_round.kills:
            if kill.attacker_name == name:
                return kill.attacker_steam_id
            elif kill.victim_name == name:
                return kill.victim_steam_id
    raise ValueError("Can't be here!")


def _get_team(name: str, rounds: List[GameRound]) -> str:
    for game_round in rounds:
        for kill in game_round.kills:
            if kill.attacker_name == name:
                return kill.attacker_team
            elif kill.victim_name == name:
                return kill.victim_team
    raise ValueError("Can't be here!")


def _get_player_kills(name: str, rounds: List[GameRound]) -> int:
    sum_of_kills = 0
    for game_round in rounds:
        kills = list(filter(lambda kill: kill.attacker_name == name
                                         and not kill.is_friendly_fire,
                            game_round.kills))
        sum_of_kills += len(kills)
    return sum_of_kills


def _get_player_death(name: str, rounds: List[GameRound]) -> int:
    sum_of_death = 0
    for game_round in rounds:
        death = list(filter(lambda kill: kill.victim_name == name and not kill.is_suicide,
                            game_round.kills))
        sum_of_death += len(death)
    return sum_of_death


def _get_player_assists(name: str, rounds: List[GameRound]) -> int:
    sum_of_assists = 0
    for game_round in rounds:
        assist = list(filter(lambda kill: kill.assister_name == name, game_round.kills))
        sum_of_assists += len(assist)
    return sum_of_assists


def _get_player_accuracy(name: str, rounds: List[GameRound]) -> int:
    count_damages = 0
    count_fire = 0
    for game_round in rounds:
        damages = list(filter(lambda damage: damage.attacker_name == name, game_round.damages))
        fires = list(filter(lambda fire: fire.name == name, game_round.weapon_fires))
        count_damages += len(damages)
        count_fire += len(fires)
    if count_damages > 0:
        return round(count_damages / count_fire * 100)
    else:
        return 0


def _get_player_headshots(name: str, rounds: List[GameRound]) -> int:
    kills_count = 0
    headshots_count = 0
    for game_round in rounds:
        kills = list(filter(lambda kill: kill.attacker_name == name, game_round.kills))
        headshots = list(filter(lambda kill: kill.attacker_name == name and kill.is_headshot,
                                game_round.kills))
        kills_count += len(kills)
        headshots_count += len(headshots)
    if kills_count > 0:
        return round(headshots_count / kills_count * 100)
    else:
        return 0


def _get_player_average_damage(name: str, rounds: List[GameRound]) -> int:
    sum_of_damage = 0
    for game_round in rounds:
        for damage in game_round.damages:
            if name == damage.attacker_name and not damage.is_friendly_fire:
                sum_of_damage += damage.hp_damage
    return round(sum_of_damage / len(rounds))


def _get_utility_damage(name: str, rounds: List[GameRound]) -> int:
    sum_of_damage = 0
    for game_round in rounds:
        for damage in game_round.damages:
            if name == damage.attacker_name and damage.attacker_weapon in GRENADES \
                    and not damage.is_friendly_fire:
                sum_of_damage += damage.hp_damage
    return sum_of_damage


def _get_KAST(name: str, rounds: List[GameRound]) -> int:
    KAST_count = 0
    for game_round in rounds:
        kills = list(filter(lambda kill: kill.attacker_name == name and not kill.is_friendly_fire, game_round.kills))
        death = list(filter(lambda kill: kill.victim_name == name and not kill.is_suicide, game_round.kills))
        assist = list(filter(lambda kill: kill.assister_name == name, game_round.kills))
        trade = list(filter(lambda kill: kill.assister_name == name and kill.is_trade, game_round.kills))
        if len(kills) != 0 or len(assist) != 0 or len(trade) != 0 or len(death) == 0:
            KAST_count += 1
    return round(KAST_count / len(rounds) * 100)


@dataclass
class KDA:
    kills: int
    death: int
    assists: int

    @classmethod
    def collect_statistics(cls, player_nickname: str, rounds: List[GameRound]) -> "KDA":
        kills = _get_player_kills(player_nickname, rounds)
        death = _get_player_death(player_nickname, rounds)
        assists = _get_player_assists(player_nickname, rounds)
        return KDA(
            kills=kills,
            death=death,
            assists=assists
        )


def _get_rating(player_KDA: KDA, ADR: int, KAST: int, rounds: int) -> float:
    average_kills = round(player_KDA.kills / rounds)
    average_death = round(player_KDA.death / rounds)
    average_assists = round(player_KDA.assists / rounds)
    impact = 2.13 * average_kills + 0.42 * average_assists - 0.41
    rating = round(0.0073 * KAST + 0.3591 * average_kills - 0.5329 * average_death
                   + 0.2372 * impact + 0.0032 * ADR + 0.1587, 3)
    return rating


@dataclass
class Player:
    steam_id: str
    name: str
    team: str
    KDA: KDA
    accuracy: int
    headshots: int
    average_damage: int
    utility_damage: int
    KAST: int
    rating: float

    @classmethod
    def collect_statistics(cls, player_nickname: str, rounds: List[GameRound]) -> "Player":
        steam_id = _get_steam_id(player_nickname, rounds)
        team = _get_team(player_nickname, rounds)
        player_KDA = KDA.collect_statistics(player_nickname, rounds)
        accuracy = _get_player_accuracy(player_nickname, rounds)
        headshots = _get_player_headshots(player_nickname, rounds)
        average_damage = _get_player_average_damage(player_nickname, rounds)
        utility_damage = _get_utility_damage(player_nickname, rounds)
        KAST = _get_KAST(player_nickname, rounds)
        rating = _get_rating(player_KDA, average_damage, KAST, len(rounds))
        return Player(
            steam_id=steam_id,
            name=player_nickname,
            team=team,
            KDA=player_KDA,
            accuracy=accuracy,
            headshots=headshots,
            average_damage=average_damage,
            utility_damage=utility_damage,
            KAST=KAST,
            rating=rating,
        )


def _print_player(player: Player):
    print()
    print(f"Игрок с никнеймом '{player.name}' из команды '{player.team}':")
    print(f"Количество убийств ................. {player.KDA.kills}", )
    print(f"Количество ассистов ................ {player.KDA.assists}")
    print(f"Количество смертей ................. {player.KDA.death}")
    print(f"Точность(%) ........................ {player.accuracy}")
    print(f"Попаданий в голову(%) .............. {player.headshots}")
    print(f"Средний урон за раунд .............. {player.average_damage}")
    print(f"Общий урон гранатами ............... {player.utility_damage}")
    print(f"KAST(%) ............................ {player.KAST}")
    print(f"Rating 2.0 ......................... {player.rating}")


def _get_score(rounds: List[GameRound]):
    teams = {}
    first_half = []
    second_half = []
    final_score = []
    for game_round in rounds:
        if game_round.round_id == 1:
            teams[game_round.winning_team] = game_round.winning_side
            if game_round.winning_side == TERRORIST_SIDE:
                teams[game_round.losing_team] = CONTER_TERRORIST_SIDE
            else:
                teams[game_round.losing_team] = TERRORIST_SIDE

        if teams.get(game_round.winning_team) != game_round.winning_side:
            if len(first_half) != 2:
                first_half.append(game_round.ct_score)
                first_half.append(game_round.t_score)

        if game_round.round_id == len(rounds):
            if game_round.winning_side == CONTER_TERRORIST_SIDE:
                final_score.append(game_round.ct_score + 1)
                final_score.append(game_round.t_score)
            else:
                final_score.append(game_round.t_score + 1)
                final_score.append(game_round.ct_score)
    second_half.append(final_score[0] - first_half[1])
    second_half.append(final_score[1] - first_half[0])

    return first_half, second_half, final_score, list(teams.keys())


@dataclass
class GameMatch:
    id: int
    map_name: str
    first_half: List[int]
    second_half: List[int]
    final_score: List[int]
    teams: List[str]
    rounds: List[GameRound]
    players: List[Player]

    @classmethod
    def from_data(cls, data: dict) -> "GameMatch":
        rounds = _fix_rounds([GameRound.from_data(it) for it in data["gameRounds"]])
        players = [Player.collect_statistics(name, rounds) for name in _get_players_nicknames(data)]
        first_half, second_half, final_score, teams = _get_score(rounds)
        return GameMatch(
            id=data["matchID"],
            map_name=data["mapName"],
            first_half=first_half,
            second_half=second_half,
            final_score=final_score,
            teams=teams,
            rounds=rounds,
            players=players
        )

    def print(self):
        _get_score(self.rounds)
        print(f"Матч '{self.id}' на карте '{self.map_name}'")
        print(f"Команды: '{self.teams[0]}' vs '{self.teams[1]}'")
        print()
        print(f"Счет в первой части игры ...... {self.first_half[0]}:{self.first_half[1]}")
        print(f"Счет во второй части игры ..... {self.second_half[0]}:{self.second_half[1]}")
        print(f"Финальный счет ................ {self.final_score[0]}:{self.final_score[1]}")
        for element in self.players:
            _print_player(element)
