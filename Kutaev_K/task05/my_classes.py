from dataclasses import dataclass
from typing import List, Type
from task05.config import *
from task05.exceptions import *


@dataclass
class WeaponFire:
    player_steam_id: int
    weapon: str
    player_team_name: str
    player_name: str

    @classmethod
    def data_to_weapon_fire(cls, weapon_fire: dict) -> "WeaponFire":
        return WeaponFire(
                    player_steam_id=weapon_fire["playerSteamID"],
                    weapon=weapon_fire["weapon"],
                    player_team_name=weapon_fire["playerTeam"],
                    player_name=weapon_fire["playerName"]
                )

    @staticmethod
    def get_weapon_fire_stats(stats: "PlayerStats",
                              weapon_fires: List["WeaponFire"],
                              player: "Player"
                              ) -> "PlayerStats":
        for weapon_fire in weapon_fires:
            if weapon_fire.player_steam_id == player.steam_id and not GRENADES.count(weapon_fire.weapon):
                stats.weapon_fires_count += 1
        return stats


@dataclass
class Damage:
    attacker_steam_id: int
    hp_damage_taken: int
    armor_damage_taken: int
    weapon: str

    @classmethod
    def data_to_damage(cls, damage: dict) -> "Damage":
        return Damage(
                    attacker_steam_id=damage["attackerSteamID"],
                    hp_damage_taken=damage["hpDamageTaken"],
                    armor_damage_taken=damage["armorDamageTaken"],
                    weapon=damage["weapon"]
                )

    @staticmethod
    def get_damage_stats(stats: "PlayerStats", damages: List["Damage"], player: "Player") -> "PlayerStats":
        for damage in damages:
            if damage.attacker_steam_id == player.steam_id:
                if GRENADES.count(damage.weapon):
                    stats.utility_damage += damage.hp_damage_taken + damage.armor_damage_taken
                else:
                    stats.weapon_damages_count += 1
                    stats.weapon_damages += damage.hp_damage_taken + damage.armor_damage_taken
        return stats


@dataclass
class Grenade:
    thrower_steam_id: int
    grenade_type: str

    @classmethod
    def data_to_grenade(cls, grenade: dict) -> "Grenade":
        return Grenade(
                    thrower_steam_id=grenade["throwerSteamID"],
                    grenade_type=grenade["grenadeType"]
                )


@dataclass
class Kill:
    attacker_steam_id: int
    victim_steam_id: int
    assister_steam_id: int
    is_suicide: int
    is_firstkill: int
    is_headshot: int
    is_trade: int
    traded_steam_id: int

    @classmethod
    def data_to_kill(cls, kill: dict) -> "Kill":
        return Kill(
                    attacker_steam_id=kill["attackerSteamID"],
                    victim_steam_id=kill["victimSteamID"],
                    assister_steam_id=kill["assisterSteamID"],
                    is_suicide=int(kill["isSuicide"]),
                    is_firstkill=int(kill["isFirstKill"]),
                    is_headshot=int(kill["isHeadshot"]),
                    is_trade=int(kill["isTrade"]),
                    traded_steam_id=kill["playerTradedSteamID"]
                )

    @staticmethod
    def get_player_stats(stats: "PlayerStats", kills: List["Kill"], player: "Player") -> "PlayerStats":
        for kill in kills:
            if kill.attacker_steam_id == player.steam_id:
                stats.kills_count += 1
                stats.is_kast = 1
                if kill.is_headshot == HEADSHOT:
                    stats.headshot_count += 1
            if kill.victim_steam_id == player.steam_id:
                stats.deaths_count += 1
                stats.is_dead_round = 1
            if kill.assister_steam_id == player.steam_id:
                stats.assist_count += 1
                stats.is_kast = 1
            if kill.traded_steam_id == player.steam_id:
                stats.is_kast = 1
            if kill == kills[LAST] and stats.is_dead_round == 0:
                stats.is_kast = 1
        return stats


@dataclass
class Round:
    number: int
    winner: str
    is_warmup: bool
    ct_team: str
    t_team: str
    kills: List[Kill]
    grenades: List[Grenade]
    damage: List[Damage]
    weapon_fires: List[WeaponFire]

    def get_round_type(self) -> int:
        if self.is_warmup is True:
            return False
        if self.winner is None:
            return False
        if self.number == CONNECTION_ROUND:
            return False
        return True

    @classmethod
    def data_to_round(cls, my_round: dict) -> "Round":
        kills_loc: List[Kill] = list()
        for kill in my_round["kills"]:
            kills_loc.append(Kill.data_to_kill(kill))

        grenades_loc: List["Grenade"] = list()
        for grenade in my_round["grenades"]:
            grenades_loc.append(Grenade.data_to_grenade(grenade))

        damages_loc: List["Damage"] = list()
        for damage in my_round["damages"]:
            damages_loc.append(Damage.data_to_damage(damage))

        weapon_fires_loc: List["WeaponFire"] = list()
        for weapon_fire in my_round["weaponFires"]:
            weapon_fires_loc.append(WeaponFire.data_to_weapon_fire(weapon_fire))
        return Round(
                    number=my_round["roundNum"],
                    winner=my_round["winningTeam"],
                    ct_team=my_round["ctTeam"],
                    t_team=my_round["tTeam"],
                    is_warmup=my_round["isWarmup"],
                    kills=kills_loc,
                    grenades=grenades_loc,
                    damage=damages_loc,
                    weapon_fires=weapon_fires_loc
                )


@dataclass
class Half:
    number: int
    rounds: List[Round]

    @classmethod
    def data_to_half(cls, good_rounds: List["Round"], half_number: int, border_round: int) -> "Half":
        if half_number == FIRST_HALF:
            return Half(
                number=FIRST_HALF,
                rounds=good_rounds[:border_round]
            )
        else:
            return Half(
                number=SECOND_HALF,
                rounds=good_rounds[border_round:]
            )

    @staticmethod
    def calc_half_stat(team_name: str, half: "Half") -> int:
        return len([my_round for my_round in half.rounds if my_round.winner == team_name])


@dataclass
class Player:
    steam_id: int
    name: str
    team_name: str

    @classmethod
    def data_to_player(cls, weapon_fire: WeaponFire) -> "Player":
        return Player(
                    steam_id=weapon_fire.player_steam_id,
                    name=weapon_fire.player_name,
                    team_name=weapon_fire.player_team_name
                )


@dataclass
class Team:
    name: str
    players: List[Player]

    @classmethod
    def data_to_team(cls, good_rounds: List[Round], match_type: int, team_name: str) -> "Team":
        if match_type == MATCH_5_X_5:
            team_players_count = TEAM_PLAYERS_COUNT_5_X_5
        else:
            team_players_count = TEAM_PLAYERS_COUNT_2_X_2

        players_steam_ids: set = set()
        for my_round in good_rounds:
            # maybe optimize it
            players_steam_ids = set(it.player_steam_id for it
                                    in my_round.weapon_fires
                                    if it.player_team_name == team_name)
            if len(players_steam_ids) == team_players_count:
                break
        players_steam_ids_list: list = list(players_steam_ids)
        players_loc: List[Player] = list()
        for my_round in good_rounds:
            for weapon_fire in my_round.weapon_fires:
                if players_steam_ids_list.count(weapon_fire.player_steam_id) and \
                        weapon_fire.player_team_name == team_name:
                    players_loc.append(Player.data_to_player(weapon_fire))

                    players_steam_ids_list.remove(weapon_fire.player_steam_id)
                    if not players_steam_ids_list:
                        if len(players_loc) < MIN_PLAYERS_COUNT:
                            raise PlayersError
                        return Team(
                            name=team_name,
                            players=players_loc
                        )
        raise PlayersSteamIDError(players_steam_ids_list)


@dataclass
class Match:
    id: int
    map: str
    type: int
    team_a: Team
    team_b: Team
    halves: List[Half]

    @classmethod
    def data_to_match(cls, data: dict) -> "Match":
        match_type_loc: int
        if data["serverVars"]["maxRounds"] == ROUND_COUNT_5_X_5:
            match_type_loc = MATCH_5_X_5
        elif data["serverVars"]["maxRounds"] == ROUND_COUNT_2_X_2:
            match_type_loc = MATCH_2_X_2
        else:
            raise MatchTypeError(data["serverVars"]["maxRounds"])

        rounds = map(lambda it: Round.data_to_round(it), data["gameRounds"])
        rounds = filter(lambda it: it.get_round_type(), rounds)
        good_rounds: List[Round] = list(rounds)
        for index, my_round in enumerate(good_rounds):
            my_round.number = index + 1

        if len(good_rounds) < MIN_GOOD_ROUNDS:
            raise GoodRoundsError
        team_a_name: str = good_rounds[FIRST_ROUND].ct_team
        team_b_name: str = good_rounds[FIRST_ROUND].t_team
        team_a_loc: Team = Team.data_to_team(good_rounds, match_type_loc, team_a_name)
        team_b_loc: Team = Team.data_to_team(good_rounds, match_type_loc, team_b_name)

        halves_loc: List[Half] = list()
        for my_round in good_rounds:
            if my_round.ct_team != team_a_name:
                halves_loc.append(Half.data_to_half(good_rounds, FIRST_HALF, my_round.number))
                halves_loc.append(Half.data_to_half(good_rounds, SECOND_HALF, my_round.number-1))

                return Match(
                    id=data["matchID"],
                    map=data["mapName"],
                    type=match_type_loc,
                    team_a=team_a_loc,
                    team_b=team_b_loc,
                    halves=halves_loc
                )
        raise TeamError(team_a_name)


@dataclass
class PlayerStats(Player):
    kills_count: int = 0

    deaths_count: int = 0
    is_dead_round: int = 0

    assist_count: int = 0

    weapon_damages_count: int = 0
    weapon_damages: int = 0
    weapon_fires_count: int = 0
    accuracy: float = 0

    headshot_count: int = 0
    hs_percent: float = 0

    average_round_damage: float = 0

    utility_damage: int = 0

    kast_count: int = 0
    kast: float = 0
    is_kast: int = 0

    rating_2_0: int = 0

    @classmethod
    def calc_player_stats(cls, halves: List["Half"], player: Player) -> "PlayerStats":
        stats: PlayerStats = PlayerStats(
            steam_id=player.steam_id,
            name=player.name,
            team_name=player.team_name,
        )

        rounds_count: int = 0

        for half in halves:
            for my_round in half.rounds:
                stats = Kill.get_player_stats(stats, my_round.kills, player)
                stats = Damage.get_damage_stats(stats, my_round.damage, player)
                stats = WeaponFire.get_weapon_fire_stats(stats, my_round.weapon_fires, player)
                if stats.is_kast == 1:
                    stats.kast_count += 1
                stats.is_kast = 0
                stats.is_dead_round = 0
                rounds_count += 1

        if stats.weapon_fires_count == 0:
            stats.weapon_fires_count = 1
            stats.weapon_damages_count = 0
        if stats.kills_count == 0:
            stats.hs_percent = 0
        else:
            stats.hs_percent = round(stats.headshot_count/stats.kills_count * IN_PERCENT, 2)
        if rounds_count == 0:
            rounds_count = 1
            stats.weapon_damages = 0
            stats.utility_damage = 0
            stats.kast_count = 0

        stats.accuracy = round(stats.weapon_damages_count / stats.weapon_fires_count * IN_PERCENT, 2)
        stats.average_round_damage = round((stats.weapon_damages + stats.utility_damage) / rounds_count, 2)
        stats.kast = round(stats.kast_count / rounds_count * IN_PERCENT, 2)
        return stats


@dataclass
class TeamStats:
    name: str
    player_stats: List[PlayerStats]
    first_half_score: int
    second_half_score: int
    final_score: int

    @classmethod
    def calc_team_stats(cls, match: Match, team: Team) -> "TeamStats":
        first_half_score_loc: int = Half.calc_half_stat(team.name, match.halves[FIRST_HALF_IN_LIST])
        second_half_score_loc: int = Half.calc_half_stat(team.name, match.halves[SECOND_HALF_IN_LIST])
        player_stats_loc: List[PlayerStats] = list()
        for player in team.players:
            player_stats_loc.append(PlayerStats.calc_player_stats(match.halves, player))
        return TeamStats(
                    name=team.name,
                    first_half_score=first_half_score_loc,
                    second_half_score=second_half_score_loc,
                    final_score=first_half_score_loc + second_half_score_loc,
                    player_stats=player_stats_loc
                )


@dataclass
class Statistics:
    team_a: TeamStats
    team_b: TeamStats

    @classmethod
    def calculate_stats(cls, match: Match) -> "Statistics":
        return Statistics(
            team_a=TeamStats.calc_team_stats(match, match.team_a),
            team_b=TeamStats.calc_team_stats(match, match.team_b)
        )

    def __iter__(self):
        yield self.team_a
        yield self.team_b
