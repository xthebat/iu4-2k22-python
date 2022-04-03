import sys
import json
from dataclasses import dataclass


class Match:
    match_id: str
    map_name: str
    team_a: str
    team_b: str
    rounds: list
    players: list

    def __init__(self):
        self.rounds = list()
        self.players = list()

    # не придумал как это лучше назвать
    # если игрок новый то добавляем его, иначе возвращаем из списка
    def add_get_player(self, player: 'Player') -> 'Player':
        if player not in self.players:
            self.players.append(player)
            return player
        else:
            return self.players[self.players.index(player)]

    def parse(self, file_name):
        with open(file_name, "rt") as file:
            text = file.read()
            data = json.loads(text)
        self.match_id = data["matchID"]
        self.map_name = data["mapName"]

        for data_round in data["gameRounds"]:
            cs_round = Round()
            cs_round.parse(data_round)

            if cs_round.is_normal():
                self.rounds.append(cs_round)

    def set_players(self):
        self.__parse_players_by_kills()
        self.__parse_players_by_damages()
        self.__parse_players_by_fires()
        self.__set_players_survive()
        self.__set_players_kast()

    def print_info(self):
        half_round = self.rounds[len(self.rounds) // 2]
        last_round = self.rounds[-1]
        count = 0
        print(f"Match {self.match_id} {self.map_name}")
        print(f"{self.rounds[0].win_team} vs {self.rounds[0].lose_team}")
        print(f"First Half:  {half_round.score._end_ct_score} : {half_round.score._end_t_score}")
        print(f"Second Half: {last_round.score._end_t_score - half_round.score._end_ct_score} :",
              f"{last_round.score._end_ct_score - half_round.score._end_t_score}")
        print(f"Final score: {last_round.score._end_t_score} : {last_round.score._end_ct_score}")
        print("     Player")
        for player in self.players:
            headshots_rate = player.headshots / player.kills if player.kills != 0 else 0
            accuracy_rate = (player.shots_done - player.shots_missed) / player.shots_done if player.shots_done != 0 else 0
            damage_rate = player.total_damage / len(self.rounds)
            kast_rate = player.kast_rounds / len(self.rounds)
            # rating 2.0
            kpr = player.kills / len(self.rounds)
            dpr = player.deaths / len(self.rounds)
            impact = 2.13 * kpr + 0.42 * player.assists / len(self.rounds) - 0.41
            rating = 0.0073 * kast_rate + 0.3591 * kpr - 0.5329 * dpr + 0.2372 * impact + 0.0032 * damage_rate + 0.1587
            print(f"{count} {player.name} {player.kills} {player.deaths} {player.assists} ",
                  f"{headshots_rate} {accuracy_rate} {damage_rate} {player.utility_damage} {kast_rate} {rating}")
            count += 1

    def __parse_players_by_kills(self):
        for cs_round in self.rounds:
            for kill in cs_round.kills:
                attacker = self.add_get_player(Player(kill.attacker_name, kill.attacker_team))
                victim = self.add_get_player(Player(kill.victim_name, kill.victim_team))
                if kill.assister_name is not None:
                    assister = self.add_get_player(Player(kill.assister_name, kill.assister_team))
                    assister.assists += 1

                attacker.shots_done += 1
                attacker.kills += 1
                victim.deaths += 1

                if kill.is_trade and kill.trader_name == attacker.name:
                    attacker.trades += 1
                elif kill.is_trade and kill.trader_name == victim.name:
                    victim.trades += 1

                if kill.is_headshot:
                    attacker.headshots += 1

    def __parse_players_by_damages(self):
        for cs_round in self.rounds:
            for damage in cs_round.damages:
                attacker = self.add_get_player(Player(damage.attacker_name, damage.attacker_team))
                vicitim = self.add_get_player(Player(damage.victim_name, damage.victim_team))

                attacker.shots_done += 1
                attacker.total_damage += damage.hp_damage_taken
                if damage.weapon == "HE Grenade" or damage.weapon == "Molotov":
                    attacker.utility_damage += damage.hp_damage_taken

    def __parse_players_by_fires(self):
        for cs_round in self.rounds:
            for fire in cs_round.fires:
                shooter = Player(fire.player_name, fire.player_team)
                shooter = self.add_get_player(shooter)
                shooter.shots_missed += 1
                shooter.shots_done += 1

    def __set_players_survive(self):
        count_of_rounds = len(self.rounds)
        for player in self.players:
            player.survives = count_of_rounds - player.deaths

    def __set_players_kast(self):
        for player in self.players:
            for cs_round in self.rounds:
                if cs_round.is_player_kast(player):
                    player.kast_rounds += 1


class Round:
    score: 'Score'
    kills: list  # List[Kill] not work..
    damages: list
    fires: list
    win_team: str
    lose_team: str

    def __init__(self):
        self.kills = list()
        self.damages = list()
        self.fires = list()

    def parse(self, data_round):
        self.score = Score(data_round)
        self.win_team = data_round["winningTeam"]
        self.lose_team = data_round["losingTeam"]
        for data_kill in data_round["kills"]:
            kill = Kill(data_kill)
            self.kills.append(kill)

        for data_damage in data_round["damages"]:
            damage = Damage(data_damage)
            self.damages.append(damage)

        for data_fire in data_round["weaponFires"]:
            fire = Fire(data_fire)
            self.fires.append(fire)

    def is_player_kast(self, player: 'Player') -> bool:
        is_kill = False
        is_assist = False
        is_survive = True
        is_trade = False
        for kill in self.kills:
            if kill.is_assister(player):
                is_assist = True
            if kill.is_trader(player):
                is_trade = True
            if kill.is_victim(player):
                is_survive = False
            if kill.is_killer(player):
                is_kill = True

        return is_kill or is_assist or is_survive or is_trade

    def is_normal(self):
        return self.score._end_t_score > self.score._t_score or \
               self.score._end_ct_score > self.score._ct_score


class Kill:
    attacker_name: str
    attacker_team: str
    victim_name: str
    victim_team: str
    assister_name: str
    assister_team: str
    trader_name: str
    is_headshot: bool
    weapon: str
    is_trade: bool

    def __init__(self, data_kill):
        self.attacker_name = data_kill["attackerName"]
        self.attacker_team = data_kill["attackerTeam"]
        self.victim_name = data_kill["victimName"]
        self.victim_team = data_kill["victimTeam"]
        self.assister_name = data_kill["assisterName"]
        self.assister_team = data_kill["assisterTeam"]
        self.trader_name = data_kill["playerTradedName"]
        self.is_headshot = data_kill["isHeadshot"]
        self.weapon = data_kill["weapon"]
        self.is_trade = data_kill["isTrade"]

    def is_assister(self, player: 'Player') -> bool:
        return self.assister_name == player.name

    def is_trader(self, player: 'Player') -> bool:
        return self.is_trade and self.trader_name == player.name

    def is_victim(self, player: 'Player') -> bool:
        return self.victim_name == player.name

    def is_killer(self, player: 'Player') -> bool:
        return self.assister_name == player.name

class Damage:
    attacker_name: str
    attacker_team: str
    victim_name: str
    victim_team: str
    hp_damage_taken: int
    weapon: str

    def __init__(self, data_damage):
        self.attacker_name = data_damage["attackerName"]
        self.attacker_team = data_damage["attackerTeam"]
        self.victim_name = data_damage["victimName"]
        self.victim_team = data_damage["victimTeam"]
        self.hp_damage_taken = data_damage["hpDamageTaken"]
        self.weapon = data_damage["weapon"]


class Fire:
    player_name: str
    player_team: str
    weapon: str

    def __init__(self, data_fire):
        self.player_name = data_fire["playerName"]
        self.player_team = data_fire["playerTeam"]
        self.weapon = data_fire["weapon"]


class Score:
    _t_score: int
    _ct_score: int
    _end_t_score: int
    _end_ct_score: int

    def __init__(self, data_round):
        self._t_score = data_round["tScore"]
        self._ct_score = data_round["ctScore"]
        self._end_t_score = data_round["endTScore"]
        self._end_ct_score = data_round["endCTScore"]


@dataclass
class Player:
    name: str
    team: str
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    survives: int = 0
    trades: int = 0
    shots_done: int = 0
    shots_missed: int = 0
    headshots: int = 0
    total_damage: int = 0
    utility_damage: int = 0
    kast_rounds: int = 0

    def __eq__(self, other):
        return self.name == other.name and self.team == other.team


def main(args):
    if len(args) < 2:
        sys.exit(-1)

    file_name = args[1]

    match = Match()
    match.parse(file_name)
    match.set_players()
    match.print_info()


if __name__ == '__main__':
    main(sys.argv)
