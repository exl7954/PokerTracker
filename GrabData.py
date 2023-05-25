import json
from Ledger import *
import time
import requests

# load game list
# dict, link:ts
with open("logs/games.json") as f:
    try:
        gameList = json.load(f)
        f.close()
    except Exception as e:
        print("Game list could not be loaded")
        print(e)

# load game data
with open("logs/gamedata.json") as f:
    try:
        gameData = json.load(f)
        f.close()
    except Exception as e:
        print("Game data could not be loaded")
        print(e)

for game in gameList:
    if game not in gameData:
        try:
            req = requests.get(f"{game}/players_sessions")
            table = Table(req.json())
        except Exception as e:
            print("Didn't grab table successfully: " + game)
            print(e)
            continue
        
        if len(table.players) <= 1:
            print("Skipping table with 1 or less players: " + game)
            time.sleep(3.5)
            continue

        # add to gameData
        currentGame = {}
        currentGame["ts"] = gameList[game]
        currentGame["ledger"] = table.getPlayers()
        gameData[game] = currentGame
        print("success: " + str(len(gameData)))
        time.sleep(3.5)

with open("logs/gamedata.json", "w") as f:
    json.dump(gameData, f)
    f.close()