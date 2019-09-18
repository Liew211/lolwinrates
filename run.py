import api_request as api

print("Summoner Name?")
summonerId = input()
print("Queue code?")
queue = int(input())
api.displayWinrates(api.getMatchList(api.getSummonerId(summonerId),queue))
