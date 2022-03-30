from dataclasses import dataclass
from typing import List
from task05.config import *
from task05.exceptions import *


@dataclass
class WeaponFire:
    player_steam_id: int
    weapon: str

    @classmethod
    def data_to_weapon_fires(cls, weapon_fire_data: list) -> List["WeaponFire"]:
        weapon_fire_list: List["WeaponFire"] = list()
        for weapon_fire in weapon_fire_data:
            weapon_fire_list.append(
                WeaponFire(
                    player_steam_id=weapon_fire["playerSteamID"],
                    weapon=weapon_fire["weapon"]
                )
            )
        return weapon_fire_list


@dataclass
class Damage:
    attacker_steam_id: int
    hp_damage_taken: int
    armor_damage_taken: int
    weapon: str

    @classmethod
    def data_to_damages(cls, damage_data: list) -> List["Damage"]:
        damage_list: List["Damage"] = list()
        for damage in damage_data:
            damage_list.append(
                Damage(
                    attacker_steam_id=damage["attackerSteamID"],
                    hp_damage_taken=damage["hpDamageTaken"],
                    armor_damage_taken=damage["armorDamageTaken"],
                    weapon=damage["weapon"]
                )
            )
        return damage_list


@dataclass
class Grenade:
    thrower_steam_id: int
    grenade_type: str

    @classmethod
    def data_to_grenades(cls, grenades_data: list) -> List["Grenade"]:
        grenades_list: List["Grenade"] = list()
        for grenade in grenades_data:
            grenades_list.append(
                Grenade(
                    thrower_steam_id=grenade["throwerSteamID"],
                    grenade_type=grenade["grenadeType"]
                )
            )
        return grenades_list


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
    def data_to_kills(cls, kills_data: list) -> List["Kill"]:
        kills_list: List["Kill"] = list()
        for kill in kills_data:
            kills_list.append(
                Kill(
                    attacker_steam_id=kill["attackerSteamID"],
                    victim_steam_id=kill["victimSteamID"],
                    assister_steam_id=kill["assisterSteamID"],
                    is_suicide=int(kill["isSuicide"]),
                    is_firstkill=int(kill["isFirstKill"]),
                    is_headshot=int(kill["isHeadshot"]),
                    is_trade=int(kill["isTrade"]),
                    traded_steam_id=kill["playerTradedSteamID"]
                )
            )
        return kills_list


@dataclass
class Round:
    number: int
    winner: str
    kills_list: List[Kill]
    grenades_list: List[Grenade]
    damage_list: List[Damage]
    weapon_fires_list: List[WeaponFire]

    @classmethod
    def is_good_round(cls, round_data: dict) -> int:
        if round_data["isWarmup"] is True:
            return INCORRECT_ROUND
        if round_data["winningSide"] == EMPTY:
            return INCORRECT_ROUND
        if round_data["roundNum"] == CONNECTION_ROUND:
            return INCORRECT_ROUND
        return GOOD_ROUND

    @classmethod
    def data_to_rounds(cls, good_rounds: list, start_round: int, end_round: int) -> List["Round"]:
        rounds_list: List["Round"] = list()
        for idx, my_round in enumerate(good_rounds):
            if start_round <= idx <= end_round:
                rounds_list.append(
                    Round(
                        number=idx,
                        winner=my_round["winningTeam"],
                        kills_list=Kill.data_to_kills(my_round["kills"]),
                        grenades_list=Grenade.data_to_grenades(my_round["grenades"]),
                        damage_list=Damage.data_to_damages(my_round["damages"]),
                        weapon_fires_list=WeaponFire.data_to_weapon_fires(my_round["weaponFires"])
                    )
                )
        return rounds_list


@dataclass
class Half:
    number: int
    ct_team: str
    t_team: str
    rounds_list: List[Round]

    @classmethod
    def data_to_halves(cls, good_rounds: list) -> List["Half"]:
        ct_team_loc = good_rounds[FIRST_ROUND]["ctTeam"]
        t_team_loc = good_rounds[FIRST_ROUND]["tTeam"]
        halves_list: List[Half] = list()
        for my_round in good_rounds:
            if my_round["ctTeam"] != ct_team_loc:
                halves_list.append(
                    Half(
                        number=FIRST_HALF,
                        ct_team=ct_team_loc,
                        t_team=t_team_loc,
                        rounds_list=Round.data_to_rounds(
                                        good_rounds,
                                        start_round=FIRST_ROUND,
                                        end_round=good_rounds.index(my_round) - 1
                                    )
                    )
                )
                halves_list.append(
                    Half(
                        number=SECOND_HALF,
                        ct_team=t_team_loc,
                        t_team=ct_team_loc,
                        rounds_list=Round.data_to_rounds(
                                        good_rounds,
                                        start_round=good_rounds.index(my_round),
                                        end_round=len(good_rounds)
                                    )
                    )
                )
                return halves_list
        raise TeamError(ct_team_loc)

    @classmethod
    def calc_half_stat(cls, team_name: str, half: "Half") -> int:
        counter: int = len([my_round for my_round in half.rounds_list if my_round.winner == team_name])
        return counter


@dataclass
class Player:
    steam_id: int
    name: str
    team_name: str

    @classmethod
    def data_to_players(cls, data_rounds: list, players_steam_ids: list) -> List["Player"]:
        players_list: List[Player] = list()

        for my_round in data_rounds:
            for weapon_fire in my_round["weaponFires"]:
                if players_steam_ids.count(weapon_fire["playerSteamID"]):
                    players_list.append(
                        Player(
                            steam_id=weapon_fire["playerSteamID"],
                            name=weapon_fire["playerName"],
                            team_name=weapon_fire["playerTeam"]
                        )
                    )
                    players_steam_ids.remove(weapon_fire["playerSteamID"])
                    if not players_steam_ids:
                        return players_list
        raise PlayersSteamIDError(players_steam_ids)

    @classmethod
    def parse_players_data(
        cls, good_rounds: list,
        first_team_name: str,
        second_team_name: str,
        match_type: int
    ) -> dict:

        if match_type == MATCH_5_X_5:
            players_count = PLAYERS_COUNT_5_X_5
        else:
            players_count = PLAYERS_COUNT_2_X_2

        players_steam_ids: set = set()
        for my_round in good_rounds:
            # maybe optimize it
            players_steam_ids = set(it["playerSteamID"] for it in my_round["weaponFires"])

            if len(players_steam_ids) == players_count:
                break

        players_list: List[Player] = Player.data_to_players(good_rounds, list(players_steam_ids))

        return_players_dict: dict = {first_team_name: [], second_team_name: []}
        for player in players_list:
            if player.team_name == first_team_name:
                return_players_dict[first_team_name].append(player)
            else:
                return_players_dict[second_team_name].append(player)
        return return_players_dict


@dataclass
class Team:
    name: str
    players_list: List[Player]

    @classmethod
    def data_to_teams(cls, good_rounds: list, match_type: int) -> List["Team"]:
        teams_list: List["Team"] = list()
        first_team_name: str = good_rounds[FIRST_ROUND]["ctTeam"]
        second_team_name: str = good_rounds[FIRST_ROUND]["tTeam"]
        player_dict: dict = Player.parse_players_data(good_rounds, first_team_name, second_team_name, match_type)
        if len(player_dict) < MIN_PLAYERS_COUNT:
            raise PlayersError
        teams_list.append(
            Team(
                name=first_team_name,
                players_list=player_dict[first_team_name]
            )
        )
        teams_list.append(
            Team(
                name=second_team_name,
                players_list=player_dict[second_team_name]
            )
        )
        return teams_list


@dataclass
class Match:
    id: int
    map: str
    type: int
    teams_list: List[Team]
    halves_list: List[Half]

    @classmethod
    def data_to_match(cls, data: dict) -> "Match":

        match_type_loc: int
        if data["serverVars"]["maxRounds"] == ROUND_COUNT_5_X_5:
            match_type_loc = MATCH_5_X_5
        elif data["serverVars"]["maxRounds"] == ROUND_COUNT_2_X_2:
            match_type_loc = MATCH_2_X_2
        else:
            raise MatchTypeError(data["serverVars"]["maxRounds"])
        good_rounds: list = [it for it in data["gameRounds"] if Round.is_good_round(round_data=it) == GOOD_ROUND]
        if len(good_rounds) < MIN_GOOD_ROUNDS:
            raise GoodRoundsError
        team_list_loc: List[Team] = Team.data_to_teams(good_rounds, match_type_loc)

        halves_list_loc: List[Half] = Half.data_to_halves(good_rounds)

        return Match(
                    id=data["matchID"],
                    map=data["mapName"],
                    type=match_type_loc,
                    teams_list=team_list_loc,
                    halves_list=halves_list_loc
        )


@dataclass
class PlayerStats(Player):
    kills_count: int
    deaths_count: int
    assist_count: int
    accuracy: float
    hs_percent: float
    average_round_damage: float
    utility_damage: int
    kast: float
    rating_2_0: int = 0

    @classmethod
    def calc_player_stats(cls, halves_list: List["Half"], player: Player) -> "PlayerStats":
        kills_count_loc: int = 0

        deaths_count_loc: int = 0
        is_dead_round: int = 0

        assist_count_loc: int = 0

        headshot_count: int = 0

        weapon_damages_count: int = 0
        weapon_damages: int = 0
        weapon_fires_count: int = 0

        grenade_damage: int = 0

        is_kast: int = 0
        kast_count: int = 0
        rounds_count: int = 0

        for half in halves_list:
            for my_round in half.rounds_list:
                for kill in my_round.kills_list:
                    if kill.attacker_steam_id == player.steam_id:
                        kills_count_loc += 1
                        is_kast = 1
                        if kill.is_headshot == HEADSHOT:
                            headshot_count += 1
                    if kill.victim_steam_id == player.steam_id:
                        deaths_count_loc += 1
                        is_dead_round = 1
                    if kill.assister_steam_id == player.steam_id:
                        assist_count_loc += 1
                        is_kast = 1
                    if kill.traded_steam_id == player.steam_id:
                        is_kast = 1
                    if kill == my_round.kills_list[LAST] and is_dead_round == 0:
                        is_kast = 1
                for damage in my_round.damage_list:
                    if damage.attacker_steam_id == player.steam_id:
                        if GRENADES.count(damage.weapon):
                            grenade_damage += damage.hp_damage_taken + damage.armor_damage_taken
                        else:
                            weapon_damages_count += 1
                            weapon_damages += damage.hp_damage_taken + damage.armor_damage_taken
                for weapon_fire in my_round.weapon_fires_list:
                    if weapon_fire.player_steam_id == player.steam_id and not GRENADES.count(weapon_fire.weapon):
                        weapon_fires_count += 1
                if is_kast == 1:
                    kast_count += 1
                is_kast = 0
                is_dead_round = 0
                rounds_count += 1

        if weapon_fires_count == 0:
            weapon_fires_count = 1
            weapon_damages_count = 0
        if kills_count_loc == 0:
            hs_percent_loc: float = 0
        else:
            hs_percent_loc: float = round(headshot_count/kills_count_loc, 3)
        if rounds_count == 0:
            rounds_count = 1
            weapon_damages = 0
            grenade_damage = 0
            kast_count = 0

        return PlayerStats(
            steam_id=player.steam_id,
            name=player.name,
            team_name=player.team_name,
            kills_count=kills_count_loc,
            deaths_count=deaths_count_loc,
            assist_count=assist_count_loc,
            accuracy=round(weapon_damages_count/weapon_fires_count * IN_PERCENT, 2),
            hs_percent=round(hs_percent_loc * IN_PERCENT, 2),
            average_round_damage=round((weapon_damages + grenade_damage)/rounds_count * IN_PERCENT, 2),
            utility_damage=grenade_damage,
            kast=round(kast_count/rounds_count * IN_PERCENT, 2)
        )

    @classmethod
    def calc_players_stats(cls, halves_list: List["Half"], team: Team) -> List["PlayerStats"]:
        player_stats_list: List[PlayerStats] = list()

        for player in team.players_list:
            player_stats_list.append(PlayerStats.calc_player_stats(halves_list, player))
        return player_stats_list


@dataclass
class TeamStats:
    name: str
    player_stats_list: List[PlayerStats]
    first_half_score: int
    second_half_score: int
    final_score: int

    @classmethod
    def calc_team_stats(cls, match: Match) -> List["TeamStats"]:
        team_stats_list: List[TeamStats] = list()
        for team in match.teams_list:
            first_half_score_loc: int = Half.calc_half_stat(team.name, match.halves_list[FIRST_HALF_IN_LIST])
            second_half_score_loc: int = Half.calc_half_stat(team.name, match.halves_list[SECOND_HALF_IN_LIST])
            team_stats_list.append(
                TeamStats(
                    name=team.name,
                    first_half_score=first_half_score_loc,
                    second_half_score=second_half_score_loc,
                    final_score=first_half_score_loc + second_half_score_loc,
                    player_stats_list=PlayerStats.calc_players_stats(match.halves_list, team)
                )
            )
        return team_stats_list


@dataclass
class Statistics:
    teams_list: List[TeamStats]

    @classmethod
    def calculate_stats(cls, match: Match) -> "Statistics":
        return Statistics(
            teams_list=TeamStats.calc_team_stats(match)
        )
