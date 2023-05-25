class Table:
    def __init__(self, data: dict):
        players = {}
        for name, pk, buy_in, buy_out, stack, net in Ledger(data["playersInfos"]):
            if pk not in players:
                players[pk] = Player(name, net)
            else:
                players[pk].net += net

        self.players = players

    def getPlayers(self):
        playerDict = {}
        for player in self.players:
            currentPlayer = {}
            currentPlayer["name"] = self.players[player].name
            currentPlayer["net"] = self.players[player].net
            playerDict[player] = currentPlayer
        return playerDict
            

class Ledger:
    def __init__(self, content: dict):
        self.content = iter(content.values())

    def __iter__(self):
        return self

    def __next__(self):
        player = next(self.content, None)
        if not player:
            raise StopIteration
        return (
            player["names"][0],
            player["id"],
            int(player["buyInSum"]),
            int(player["buyOutSum"]),
            int(player["inGame"]),
            int(player["net"]),
        )

class Player:
    def __init__(self, name: str, net: int):
        self.name = name
        self.net = net

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}: {self.net}"