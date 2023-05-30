import json

with open("logs/gamedata.json") as f:
    gameData = json.load(f)
    f.close()

with open("logs/names.json") as f:
    NAMES = json.load(f)
    f.close()

players = {}
newPlayers = {}
for game in gameData:
    currentGame = gameData[game]
    for player in currentGame["ledger"].values():
        match = False

        for name in NAMES.items():
            if player["name"].lower() in name[1]:
                if name[0] not in players:
                    players[name[0]] = player["net"]
                    match=True
                    break
                else:
                    players[name[0]] += player["net"]
                    match=True
                    break

        if (match==False):
            if player["name"].lower() not in newPlayers:
                newPlayers[player["name"].lower()] = player["net"]
            else:
                newPlayers[player["name"].lower()] += player["net"]
        


newPlayers = sorted(newPlayers.items(), key=lambda x:abs(x[1]), reverse=True)
for player in newPlayers:
    print(player)

