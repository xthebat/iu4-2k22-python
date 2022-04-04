import enum
from dataclasses import dataclass, field
from typing import Iterable, List


@dataclass
class Player:
    name: str
    team: str


@dataclass
class PlayerStatistics:
    player: "Player"
    kills: List["KillAction"]
    deaths: List["KillAction"]
    assists: List["KillAction"]
    damages_by_round: List[List["DamageAction"]]
    weapon_fires: List["WeaponFireAction"]

    @property
    def damages(self) -> List["DamageAction"]:
        damages = list()
        for damages_in_round in self.damages_by_round:
            for damage in damages_in_round:
                damages.append(damage)
        return damages

    @property
    def headshot_kills(self) -> List["KillAction"]:
        return [kill for kill in self.kills if kill.is_headshot]

    @property
    def kills_count(self) -> int:
        return len(self.kills)

    @property
    def deaths_count(self) -> int:
        return len(self.deaths)

    @property
    def assists_count(self) -> int:
        return len(self.assists)

    @property
    def accuracy_rate(self) -> float:
        if len(self.weapon_fires) == 0:
            return .0
        return len(self.damages) / len(self.weapon_fires)

    @property
    def headshot_rate(self) -> float:
        if len(self.kills) == 0:
            return .0
        return len(self.headshot_kills) / len(self.kills)

    @property
    def average_damage_by_round(self) -> float:
        average_round_damage_sum = .0
        for damages_in_round in self.damages_by_round:
            average_round_damage = .0
            for damage in damages_in_round:
                average_round_damage += damage.hp_damage_taken
            if len(damages_in_round) != 0:
                average_round_damage_sum += average_round_damage / len(damages_in_round)
        if len(self.damages_by_round) != 0:
            return average_round_damage_sum / len(self.damages_by_round)
        else:
            return .0

    @property
    def utility_damage(self) -> int:
        damage_sum = 0
        for damage in self.damages:
            if damage.weapon in Weapons.grenades.value:
                damage_sum += damage.hp_damage_taken
        return damage_sum


@dataclass
class Match:
    match_id: str
    map_name: str
    rounds: List["Round"]

    @property
    def teams(self) -> List["Team"]:
        teams = list()
        players = self.players
        for player in players:
            if Team(player.team) not in teams:
                teams.append(Team(player.team))
            teams[teams.index(Team(player.team))].players.append(player)
        for match_round in self.game_rounds:
            if match_round.round_type == Round.RoundType.first_half:
                teams[teams.index(Team(match_round.winning_team))].first_half_score += 1
            if match_round.round_type == Round.RoundType.second_half:
                teams[teams.index(Team(match_round.winning_team))].second_half_score += 1
        return teams

    @property
    def players(self) -> List["Player"]:
        players = list()
        for match_round in self.rounds:
            for damage in match_round.damages:
                if damage.attacker not in players and damage.attacker.name is not None:
                    players.append(damage.attacker)
        return players

    @property
    def game_rounds(self) -> List["Round"]:
        return [match_round for match_round in self.rounds if
                match_round.round_type in [Round.RoundType.first_half, Round.RoundType.second_half]]

    @classmethod
    def from_dict(cls, match_dict: dict) -> "Match":
        match_id = match_dict["matchID"]
        map_name = match_dict["mapName"]
        match_team_switch_time = match_dict["matchPhases"]["teamSwitch"][0]
        rounds = list()

        rounds_list = match_dict["gameRounds"]
        for round_dict in rounds_list:
            match_round = Round.from_dict(round_dict)
            if match_round.round_type == Round.RoundType.unknown:
                if round_dict["startTick"] < match_team_switch_time:
                    match_round.round_type = Round.RoundType.first_half
                else:
                    match_round.round_type = Round.RoundType.second_half
            rounds.append(match_round)

        return cls(
            match_id=match_id,
            map_name=map_name,
            rounds=rounds,
        )

    def print_statistics(self) -> None:
        print(f"Match {self.match_id} {self.map_name}")
        teams = self.teams
        print(f"{teams[0].name} vs {teams[1].name}")
        for match_round in self.rounds:
            if match_round.round_type == match_round.RoundType.knife:
                print(f"Knife round winner: {match_round.winning_team}")
                break

        print(f"First Half: {teams[0].first_half_score}:{teams[1].first_half_score}")
        print(f"Second Half: {teams[0].second_half_score}:{teams[1].second_half_score}")
        print(f"Final Score: {teams[0].score}:{teams[1].score}")
        players = self.players

        print(
            f"{' ':>2}",
            f"{'Player':>15}",
            f"{'K':>2}",
            f"{'D':>2}",
            f"{'A':>2}",
            f"{'ACC%' * 100:>6.3}",
            f"{'HS%' * 100:>6.3}",
            f"{'ADR':>6.3}",
            f"{'UD':>3}",
        )
        for i, player in enumerate(players):
            statistics = self.get_player_statistics(player)
            print(
                f"{i + 1:>2}",
                f"{statistics.player.name:>15}",
                f"{statistics.kills_count:>2}",
                f"{statistics.deaths_count:>2}",
                f"{statistics.assists_count:>2}",
                f"{statistics.accuracy_rate * 100:>6.3}",
                f"{statistics.headshot_rate * 100:>6.3}",
                f"{statistics.average_damage_by_round:>6.3}",
                f"{statistics.utility_damage:>3}",
            )

    def get_player_statistics(self, player: "Player") -> PlayerStatistics:
        kills = list()
        deaths = list()
        assists = list()
        damages_by_round = list()
        weapon_fires = list()

        for match_round in self.game_rounds:
            for kill in match_round.kills:
                if kill.attacker == player:
                    kills.append(kill)
                if kill.victim == player:
                    deaths.append(kill)
                if kill.assister == player:
                    assists.append(kill)
            damages_in_round = list()
            for damage in match_round.damages:
                if damage.attacker == player:
                    damages_in_round.append(damage)
            damages_by_round.append(damages_in_round)
            for weapon_fire in match_round.weapon_fires:
                if weapon_fire.player == player:
                    weapon_fires.append(weapon_fire)

        return PlayerStatistics(
            player=player,
            kills=kills,
            deaths=deaths,
            assists=assists,
            damages_by_round=damages_by_round,
            weapon_fires=weapon_fires
        )


@dataclass
class Team:
    name: str
    first_half_score: int = 0
    second_half_score: int = 0
    players: List["Player"] = field(default_factory=list)

    @property
    def score(self) -> int:
        return self.first_half_score + self.second_half_score

    def __eq__(self, __o: "Team") -> bool:
        return self.name == __o.name

    def __iter__(self) -> Iterable["Player"]:
        return iter(self.players)


@dataclass
class Round:
    round_type: "RoundType"
    num: int
    winning_team: str
    kills: List["KillAction"]
    damages: List["DamageAction"]
    grenades: List["GrenadeAction"]
    weapon_fires: List["WeaponFireAction"]

    class RoundType(enum.Enum):
        knife = 'Knife'
        warmup = 'Warmup'
        system = 'System'
        first_half = 'First Half'
        second_half = 'Second Half'
        unknown = 'Unknown'

    @classmethod
    def from_dict(cls, round_dict: dict) -> "Round":
        num = round_dict["roundNum"]
        winning_team = round_dict["winningTeam"]
        kills = list()
        damages = list()
        grenades = list()
        weapon_fires = list()
        kill_weapons = set()
        for kill_dict in round_dict["kills"]:
            kill = KillAction.from_dict(kill_dict)
            kill_weapons.add(kill.weapon)
            kills.append(kill)
        for damage_dict in round_dict["damages"]:
            damages.append(DamageAction.from_dict(damage_dict))
        for grenade_dict in round_dict["grenades"]:
            grenades.append(GrenadeAction.from_dict(grenade_dict))
        for weapon_fires_dict in round_dict["weaponFires"]:
            weapon_fires.append(WeaponFireAction.from_dict(weapon_fires_dict))

        if len(kill_weapons) == 1 and "Knife" in kill_weapons:
            round_type = cls.RoundType.knife
        elif round_dict["isWarmup"]:
            round_type = cls.RoundType.warmup
        elif round_dict["endTick"] == 0:
            round_type = Round.RoundType.system
        else:
            round_type = Round.RoundType.unknown

        return cls(
            round_type=round_type,
            num=num,
            winning_team=winning_team,
            kills=kills,
            damages=damages,
            grenades=grenades,
            weapon_fires=weapon_fires
        )


class Weapons(enum.Enum):
    grenades = ["HE Grenade", "Incendiary Grenade"]


@dataclass
class KillAction:
    attacker: "Player"
    victim: "Player"
    assister: "Player"
    is_headshot: bool
    weapon: str

    @classmethod
    def from_dict(cls, kill_dict: dict) -> "KillAction":
        return cls(
            attacker=Player(
                name=kill_dict["attackerName"],
                team=kill_dict["attackerTeam"]
            ),
            victim=Player(
                name=kill_dict["victimName"],
                team=kill_dict["victimTeam"]
            ),
            assister=Player(
                name=kill_dict["assisterName"],
                team=kill_dict["assisterTeam"]
            ),
            is_headshot=kill_dict["isHeadshot"],
            weapon=kill_dict["weapon"],
        )


@dataclass
class DamageAction:
    attacker: "Player"
    victim: "Player"
    hp_damage_taken: int
    weapon: str

    @classmethod
    def from_dict(cls: "DamageAction", damage_dict: dict) -> "DamageAction":
        return cls(
            attacker=Player(
                damage_dict["attackerName"],
                damage_dict["attackerTeam"]
            ),
            victim=Player(
                damage_dict["victimName"],
                damage_dict["victimTeam"]
            ),
            hp_damage_taken=damage_dict["hpDamageTaken"],
            weapon=damage_dict["weapon"]
        )


@dataclass
class GrenadeAction:
    thrower: "Player"
    grenade_type: str

    @classmethod
    def from_dict(cls, grenade_dict: dict) -> "GrenadeAction":
        return cls(
            thrower=Player(
                grenade_dict["throwerName"],
                grenade_dict["throwerTeam"]
            ),
            grenade_type=grenade_dict["grenadeType"],
        )


@dataclass
class WeaponFireAction:
    player: "Player"
    weapon: str

    @classmethod
    def from_dict(cls, weapon_fire_dict: dict) -> "WeaponFireAction":
        return cls(
            player=Player(
                name=weapon_fire_dict["playerName"],
                team=weapon_fire_dict["playerTeam"]
            ),
            weapon=weapon_fire_dict["weapon"]
        )
