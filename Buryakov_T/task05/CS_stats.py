from dataclasses import dataclass
from typing import List

INVALID_STEAM_ID = 0
PERCENT = 100
GRENADE = ["Molotov", "Smoke Grenade", "HE Grenade", "Incendiary Grenade", "Flashbang", "Decoy Grenade"]
CT_SIDE = "CT"
T_SIDE = "T"


@dataclass
class Kill:
    attacker_steam_id: int
    attacker_name: str
    attacker_team: str
    victim_steam_id: int
    victim_name: str
    victim_team: str
    assister_steam_id: int
    assister_name: str
    assister_team: str
    is_suicide: bool
    is_team_kill: bool
    is_trade: bool
    weapon: str

    @classmethod
    def from_data(cls, data: dict) -> "Kill":
        return Kill(
            attacker_steam_id=data["attackerSteamID"],
            attacker_name=data["attackerName"],
            attacker_team=data["attackerTeam"],
            victim_steam_id=data["victimSteamID"],
            victim_name=data["victimName"],
            victim_team=data["victimTeam"],
            assister_steam_id=data["assisterSteamID"],
            assister_name=data["assisterName"],
            assister_team=data["assisterTeam"],
            is_suicide=data["isSuicide"],
            is_team_kill=data["isTeamkill"],
            is_trade=data["isTrade"],
            weapon=data["weapon"]
        )


@dataclass
class WeaponFire:
    player_steam_id: int

    @classmethod
    def from_data(cls, data: dict) -> "WeaponFire":
        return WeaponFire(
            player_steam_id=data["playerSteamID"]
        )


@dataclass
class Damage:
    attacker_steam_id: int
    victim_steam_id: int
    weapon: str
    hp_damage_taken: int
    hit_group: str
    is_friendly_fire: bool

    @classmethod
    def from_data(cls, data: dict) -> "Damage":
        return Damage(
            attacker_steam_id=data["attackerSteamID"],
            victim_steam_id=data["victimSteamID"],
            weapon=data["weapon"],
            hp_damage_taken=data["hpDamageTaken"],
            hit_group=data["hitGroup"],
            is_friendly_fire=data["isFriendlyFire"]
        )


@dataclass
class Round:
    num: int
    is_warmup: bool
    t_score: int
    ct_score: int
    winning_side: str
    winning_team: str
    losing_team: str
    kills: List[Kill]
    damages: List[Damage]
    weapon_fires: List[WeaponFire]

    @classmethod
    def from_data(cls, data: dict) -> "Round":
        kills_data = [Kill.from_data(it) for it in data["kills"]]
        damages = [Damage.from_data(it) for it in data["damages"]]
        weapon_fires = [WeaponFire.from_data(it) for it in data["weaponFires"]]
        return Round(
            num=data["roundNum"],
            is_warmup=data["isWarmup"],
            t_score=data["tScore"],
            ct_score=data["ctScore"],
            winning_side=data["winningSide"],
            winning_team=data["winningTeam"],
            losing_team=data["losingTeam"],
            kills=kills_data,
            damages=damages,
            weapon_fires=weapon_fires
        )


@dataclass
class Player:
    steam_id: int
    name: str
    team: str

    @staticmethod
    def _name_info(steam_id: int, game_rounds: list):
        for game_round in game_rounds:
            for kill in game_round.kills:
                if steam_id == kill.attacker_steam_id:
                    return kill.attacker_name, kill.attacker_team
                elif steam_id == kill.victim_steam_id:
                    return kill.victim_name, kill.victim_team
                elif steam_id == kill.assister_steam_id:
                    return kill.assister_name, kill.assister_team
        raise KeyError("Name and team isn't found")


@dataclass
class Statistics(Player):
    kills: int
    death: int
    assist: int
    acc: float
    hs: float
    adr: float
    ud: float
    kast: float
    rating_2_0: float

    @classmethod
    def from_data(cls, steam_id: int, game_rounds: List[Round]):
        name, team = cls._name_info(steam_id, game_rounds)
        kills, death, assist = cls._sum_of_kda(steam_id, game_rounds)
        acc, hs, adr, grenade_dmg = cls.calculation_acc_hs_adr_grenade(steam_id, game_rounds)
        kast = cls._calc_kast(steam_id, game_rounds)
        rating_2_0 = cls._find_rating_2_0(kast, kills, death, assist, adr, len(game_rounds))
        return Statistics(
            steam_id=steam_id,
            name=name,
            team=team,
            kills=kills,
            death=death,
            assist=assist,
            acc=round(acc, 2),
            hs=round(hs, 2),
            adr=round(adr, 2),
            ud=round(grenade_dmg, 2),
            kast=round(kast, 2),
            rating_2_0=round(rating_2_0, 2)
        )

    @staticmethod
    def _sum_of_kda(steam_id: int, game_rounds: list):
        player_kills = 0
        player_death = 0
        player_assist = 0
        for game_round in game_rounds:
            for kill in game_round.kills:
                if steam_id == kill.attacker_steam_id and not kill.is_team_kill:
                    player_kills += 1
                elif steam_id == kill.victim_steam_id:
                    player_death += 1
                elif steam_id == kill.assister_steam_id:
                    player_assist += 1
        return player_kills, player_death, player_assist

    @staticmethod
    def calculation_acc_hs_adr_grenade(steam_id: int, game_rounds: list):
        count_of_fires = 0
        count_of_damages = 0
        hs_count = 0
        adr_count = 0
        grenade_dmg = 0.0
        for game_round in game_rounds:
            for fire in game_round.weapon_fires:
                if steam_id == fire.player_steam_id:
                    count_of_fires += 1
            for damage in game_round.damages:
                if steam_id == damage.attacker_steam_id and damage.is_friendly_fire is False:
                    if damage.hit_group == "Head":
                        hs_count += 1
                    if damage.weapon in GRENADE:
                        grenade_dmg += damage.hp_damage_taken
                    count_of_damages += 1
                    adr_count += damage.hp_damage_taken
        match_acc = count_of_damages / count_of_fires * PERCENT
        match_hs = hs_count / count_of_fires * PERCENT
        adr_count = adr_count / len(game_rounds)
        return match_acc, match_hs, adr_count, grenade_dmg

    @staticmethod
    def _calc_kast(steam_id: int, game_rounds: list):
        kast_count = 0
        survive = 1
        for game_round in game_rounds:
            for kill in game_round.kills:
                if steam_id == kill.attacker_steam_id and not kill.is_team_kill:
                    kast_count += 1
                    break
                elif steam_id == kill.assister_steam_id:
                    kast_count += 1
                    break
                elif steam_id == kill.victim_steam_id and kill.is_trade:
                    kast_count += 1
                    break
                elif steam_id == kill.victim_steam_id and not kill.is_trade:
                    survive = 0
            if survive == 1:
                kast_count += 1
        return kast_count / len(game_rounds) * PERCENT

    @staticmethod
    def _find_rating_2_0(kast: float, kills: int, deaths: int, assists: int, adr: float, count_of_rounds: int):
        kpr = kills / count_of_rounds
        dpr = deaths / count_of_rounds
        apr = assists / count_of_rounds
        impact = 2.13 * kpr + 0.42 * apr - 0.41
        return 0.0073 * kast + 0.3591 * kpr - 0.5329 * dpr + 0.2372 * impact + 0.0032 * adr + 0.1587


@dataclass
class Match:
    match_id: str
    map_name: str
    win_team_info: list
    lose_team_info: list
    game_rounds: List[Round]
    statistics: List[Statistics]

    @classmethod
    def from_data(cls, data: dict, fix_rounds: bool = True) -> "Match":
        game_rounds = [Round.from_data(it) for it in data["gameRounds"]]
        if fix_rounds:
            game_rounds = cls._fix_rounds(game_rounds)
        statistics = [Statistics.from_data(it, game_rounds) for it in cls._list_of_steam_id(data)]
        win_team_info, lose_team_info = cls._take_teams_and_score(game_rounds)
        return Match(
            match_id=data["matchID"],
            map_name=data["mapName"],
            win_team_info=win_team_info,
            lose_team_info=lose_team_info,
            game_rounds=game_rounds,
            statistics=statistics
        )

    def print(self):
        print('\n'.join(str(it) for it in self.statistics))
        print('\n'.join(str(it) for it in self.game_rounds))

    def print_statistics(self):
        print(f"Match {self.match_id} MAP: {self.map_name}")
        print(f"{self.win_team_info[0]} VS {self.lose_team_info[0]}")
        print("First half: {w:6d} : {l:d}".format(w=self.win_team_info[1], l=self.lose_team_info[1]))
        print("Second half: {w:5d} : {l:d}".format(w=self.win_team_info[2] - self.win_team_info[1],
                                                   l=self.lose_team_info[2] - self.lose_team_info[1]))
        print("Final score: {w:5d} : {l:d}".format(w=self.win_team_info[2], l=self.lose_team_info[2]))
        print("-" * 96)
        print("%12s %16s %3s %3s %3s %7s %7s %8s %7s %8s %12s" %
              ("Player", "Team", "K", "D", "A", "ACC%", "HS%", "ADR", "UD", "KAST%", "Rating 2.0"))
        for pl in self.statistics:
            print("%12s %16s %3d %3d %3d %7.2f %7.2f %8.2f %7.2f %8.2f %12.2f" %
                  (pl.name, pl.team, pl.kills, pl.death, pl.assist, pl.acc, pl.hs, pl.adr, pl.ud, pl.kast,
                   pl.rating_2_0))

    def print_statistics_in_file(self):
        with open("results analysis.txt", "w") as f:
            print(f"Match {self.match_id} MAP: {self.map_name}", file=f)
            print(f"{self.win_team_info[0]} VS {self.lose_team_info[0]}", file=f)
            print("First half: {w:6d} : {l:d}".format(w=self.win_team_info[1], l=self.lose_team_info[1]), file=f)
            print("Second half: {w:5d} : {l:d}".format(w=self.win_team_info[2] - self.win_team_info[1],
                                                       l=self.lose_team_info[2] - self.lose_team_info[1]), file=f)
            print("Final score: {w:5d} : {l:d}".format(w=self.win_team_info[2], l=self.lose_team_info[2]), file=f)
            print("-" * 96, file=f)
            print("%12s %16s %3s %3s %3s %7s %7s %8s %7s %8s %12s" %
                  ("Player", "Team", "K", "D", "A", "ACC%", "HS%", "ADR", "UD", "KAST%", "Rating 2.0"), file=f)
            for pl in self.statistics:
                print("%12s %16s %3d %3d %3d %7.2f %7.2f %8.2f %7.2f %8.2f %12.2f" %
                      (pl.name, pl.team, pl.kills, pl.death, pl.assist, pl.acc, pl.hs, pl.adr, pl.ud, pl.kast,
                       pl.rating_2_0), file=f)

    @staticmethod
    def _list_of_steam_id(data: dict):
        steam_ids = set()
        player_connections = data["playerConnections"]
        for connection in player_connections:
            steam_id = connection["steamID"]
            if steam_id != INVALID_STEAM_ID:
                steam_ids.add(steam_id)
        return list(steam_ids)

    @staticmethod
    def _get_start_index(rounds: List[Round]):
        for index, game_round in enumerate(reversed(rounds)):
            if game_round.t_score == 0 and game_round.ct_score == 0:
                return len(rounds) - index - 1
        raise IndexError("Can't find valid start found")

    @classmethod
    def _fix_rounds(cls, rounds: List[Round]):
        start_index = cls._get_start_index(rounds)
        start_number = rounds[start_index].num - 1
        result = rounds[start_index:]
        for it in result:
            it.num -= start_number
        return list(it for it in result if it.winning_team is not None)

    @staticmethod
    def _take_teams_and_score(game_rounds: list):
        teams = {}
        for game_round in game_rounds:
            teams.setdefault(game_round.winning_team, game_round.winning_side)
            if game_round.winning_side == T_SIDE:
                teams.setdefault(game_round.losing_team, CT_SIDE)
            else:
                teams.setdefault(game_round.losing_team, T_SIDE)

            if teams[game_round.winning_team] != game_round.winning_side:
                teams.setdefault(CT_SIDE, [game_round.ct_score])
                teams.setdefault(T_SIDE, [game_round.t_score])

            if game_round.num == len(game_rounds):
                if game_round.winning_side == CT_SIDE:
                    teams[CT_SIDE].append(game_round.ct_score + 1)
                    teams[T_SIDE].append(game_round.t_score)
                    win_team_info = [game_round.winning_team, teams[CT_SIDE][0], teams[CT_SIDE][1]]
                    lose_team_info = [game_round.losing_team, teams[T_SIDE][0], teams[T_SIDE][1]]
                    return win_team_info, lose_team_info
                else:
                    teams[CT_SIDE].append(game_round.ct_score)
                    teams[T_SIDE].append(game_round.t_score + 1)
                    win_team_info = [game_round.winning_team, teams[T_SIDE][0], teams[T_SIDE][1]]
                    lose_team_info = [game_round.losing_team, teams[CT_SIDE][0], teams[CT_SIDE][1]]
                    return win_team_info, lose_team_info

    @staticmethod
    def _take_teams_and_score_bad(game_rounds: list):
        number_of_rounds = len(game_rounds)
        first_half = 8
        score_team_a = 0
        score_team_b = 0
        half_score_team_a = 0
        half_score_team_b = 0
        for game_round in game_rounds:
            if game_round.winning_side == "CT" and game_round.num <= first_half:
                score_team_a += 1
            elif game_round.winning_side == "T" and game_round.num <= first_half:
                score_team_b += 1
            if game_round.num == first_half:
                half_score_team_a = score_team_a
                half_score_team_b = score_team_b
            if game_round.winning_side == "CT" and game_round.num > first_half:
                score_team_b += 1
            elif game_round.winning_side == "T" and game_round.num > first_half:
                score_team_a += 1
            if game_round.num == number_of_rounds:
                if game_round.winning_side == "CT":  # Winning team B
                    list_win_team = [game_round.winning_team, half_score_team_b, score_team_b]
                    list_lose_team = [game_round.losing_team, half_score_team_a, score_team_a]
                    return list_win_team, list_lose_team
                else:  # Winning team A
                    list_win_team = [game_round.winning_team, half_score_team_a, score_team_a]
                    list_lose_team = [game_round.losing_team, half_score_team_b, score_team_b]
                    return list_win_team, list_lose_team
