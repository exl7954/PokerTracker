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
        

players = sorted(players.items(), key=lambda x:x[1], reverse=True)
for player in players:
    print(player)

