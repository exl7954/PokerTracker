import os
import json

with open("logs/names.json") as f:
    NAMES = json.load(f)
    f.close()

def matchName(s):
    if s in NAMES.keys():
        return s
    
    s = s.lower()
    for name in NAMES:
        if s in NAMES[name]:
            return name
    return s

def getGraph():
    with open("logs/graph.json") as f:
        graph = json.load(f)
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

    

    start = matchName(start)
    graph = getGraph()
    res = {}
    for player in end:
        player = matchName(player)
        arr = find_shortest_path(graph, start, player)
        if arr is None:
            pass
        else:
            res[player] = len(arr)
        
    
    res = sorted(res.keys(), key=lambda x:res[x])
    return res
        
