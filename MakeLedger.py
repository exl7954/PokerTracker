import json
import requests
from Ledger import *
from PlayerChain import findPaths, matchName

def makeLedger(uri: str):
    if not uri.startswith("https://"):
        uri = "https://" + uri
    if not "https://www.pokernow.club/games/" in uri:
        return

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 'Referer': 'https://l.messenger.com/'}
    req = requests.get(uri+"/players_sessions", headers=headers)
    if not req.status_code == 200:
        print(req.status_code)
        return

    table = Table(req.json())
    ledger = table.getPlayers()
    lines = []

    winners = {}
    losers = {}
    for id in ledger:
        player = ledger[id]
        if player["net"] > 0:
            winners[player["name"]] = player["net"]
        if player["net"] < 0:
            losers[player["name"]] = player["net"]

    winners = dict(sorted(winners.items(), key=lambda x:x[1], reverse=True))
    losers = dict(sorted(losers.items(), key=lambda x:x[1], reverse=False))

    taxes = []
    for winner in winners:
        tax = winners[winner] / 2000
        if (tax > 10):
            taxes.append(winner + " pays paul $10.00")
        elif (tax > 0.01):
            taxes.append(winner + " pays paul $%.2f" % tax)

    """
    for player in losers:
        print(player + ": " + str(findPaths(player, winners)))
        print()
    """

    preferredMatches = {}
    for player in losers.keys():
        arr = findPaths(player, winners.keys())
        if len(arr) >= 1:
            preferredMatches[player] = arr

    ## CREATE LEDGER (preferred)

    for loser in losers:
        if loser in preferredMatches.keys():
            for winner in preferredMatches[loser]:
                #reverse match name
                for w in winners:
                    if matchName(w) == winner:
                        winner = w
                        break


                if winners[winner] >= abs(losers[loser]) and losers[loser] != 0:
                    amt = -losers[loser]
                    winners[winner] += losers[loser]
                    losers[loser] = 0
                    lines.append(loser + " pays " + winner + " $%.2f" % (amt/100))
                elif winners[winner] < abs(losers[loser]) and winners[winner] != 0: # WINNER < LOSER
                    amt = winners[winner]
                    losers[loser] += winners[winner]
                    winners[winner] = 0
                    lines.append(loser + " pays " + winner + " $%.2f" % (amt/100))

                if losers[loser] == 0:
                    break

    # CREATE LEDGER (non-preferred)
    for loser in losers:
        while losers[loser] != 0:

            for winner in winners:
                if winners[winner] == 0:
                    continue

                if winners[winner] >= abs(losers[loser]):
                    amt = -losers[loser]
                    winners[winner] += losers[loser]
                    losers[loser] = 0
                    lines.append(loser + " pays " + winner + " $%.2f" % (amt/100))
                    break
                else:
                    amt = winners[winner]
                    losers[loser] += winners[winner]
                    winners[winner] = 0
                    lines.append(loser + " pays " + winner + " $%.2f" % (amt/100))
                    break


    if max(winners.values()) != 0 and max(losers.values() != 0):
        return("BIG error")
    else:
        res = ""
        for l in lines:
            res += l + "\n"
        res += "\n"
        res += "TAXES\n"
        for l in taxes:
            res += l + "\n"

        return res
