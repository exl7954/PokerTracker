import os
import json

def getGraph():
    # get all json files in directory
    PATH = "logs/chat-logs/"
    FILES = [f for f in os.listdir(PATH) if f.endswith('.json')]

    # dict, added:[adder,ts]
    addHistory = {}
    # dict, name:msgsSent
    participants = {}

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

        for user in data["participants"]:
            user = user["name"]
            if user not in participants:
                participants[user] = 0

        for msg in data["messages"]:
            if msg["sender_name"] not in participants:
                participants[msg["sender_name"]] = 1
            else:
                participants[msg["sender_name"]] += 1
            if "content" in msg and "added" in msg["content"] and "to the group." in msg["content"]:
                for user in msg["users"]:
                    user = user["name"]
                    if user in addHistory.keys():
                        if msg["timestamp_ms"] < addHistory[user][1]:
                            addHistory[user][0] = msg["sender_name"]
                            addHistory[user][1] = msg["timestamp_ms"]
                    else:
                        toAdd = []
                        toAdd.append(msg["sender_name"])
                        toAdd.append(msg["timestamp_ms"])
                        addHistory[user] = toAdd


    participants = sorted(participants.items(), key=lambda x:x[1], reverse=True)
    graph = {}
    for user in addHistory:
        adder = addHistory[user][0]
        graph[user] = [adder]

    for user in graph:
        adder = graph[user][0]
        if adder in graph and user not in graph[adder]:
            graph[adder].append(user)
            

    # print unaccounted for users
    """
    for user in participants:
        if user[0] not in addHistory:
            print(user)
    """
    
    
    # graph test
    """
    for user in graph:
    print(user)

    while True:
        q = input()
        if (q == "exit"):
            break

        q = q.split("|")
        print(find_shortest_path(graph, q[0], q[1]))
    """

    return graph

def findPaths(start, end):
    def find_shortest_path(graph, start, end, path=[]):
            path = path + [start]
            if start == end:
                return path
            if start not in graph.keys():
                return None
            shortest = None
            for node in graph[start]:
                if node not in path:
                    newpath = find_shortest_path(graph, node, end, path)
                    if newpath:
                        if not shortest or len(newpath) < len(shortest):
                            shortest = newpath
            return shortest

    graph = getGraph()
    res = {}
    for player in end:
        arr = find_shortest_path(graph, start, player)
        if arr is None:
            length = 100
        else:
            length = len(arr)
        
        res[player] = length
    
    res = sorted(res.items, key=lambda x:x[1])
        