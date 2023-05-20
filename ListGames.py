import os
import json

# get all json files in directory
PATH = "logs/chat-logs/"
FILES = [f for f in os.listdir(PATH) if f.endswith('.json')]

# load existingGames dict from file if exists, or create one
if (os.path.isfile("logs/games.json")):
    try:
        file = open("logs/games.json")
        existingGames = json.load(file)
        file.close()
    except Exception as e:
        print("existing games json could not be loaded")
        print(e)
        existingGames = {}
else:
    existingGames = {}


for f in FILES:
    try:
        filePath = "logs/chat-logs/" + f
        openFile = open(filePath)
        data = json.load(openFile)
        openFile.close()
    except Exception as e:
        print(filePath + " could not be json loaded")
        print(e)

    if ("participants" not in data and "messages" not in data):
        print(filePath + " has incorrect json format")
        continue

    for msg in data["messages"]:
        if "content" in msg and "www.pokernow.club/games/" in msg["content"]:
            #format link
            link = msg["content"]
            if '?' in link:
                link = link[0:link.index('?')]

            if link not in existingGames:
                existingGames[link] = msg["timestamp_ms"]


print(len(existingGames))

file = open("logs/games.json", "w")
json.dump(existingGames, file)
file.close()