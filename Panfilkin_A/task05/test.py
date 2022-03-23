from CS import Player
import json
FILENAME = "t1.json"

with open(FILENAME, "r") as f:
    data = json.load(f)

rounds = data["gameRounds"]
team_switch_time = data["matchPhases"]["teamSwitch"][0]

for round in rounds:
    is_warmup = round["isWarmup"]
    halve = 1 if round["startTick"] < team_switch_time else 2
    print(round["roundNum"], halve, round["ctTeam"], round["tTeam"], is_warmup)