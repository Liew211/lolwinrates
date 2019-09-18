import api_request as api

# Switch statement for queue type
def switch(queue):
    switcher = {
        'blind': 430,
        'draft': 400,
        'solo': 420,
        'flex': 440
    }
    return switcher.get(queue, 0)

# Prompt user for inputs
print("Summoner Name?")
summonerId = input()

queueCode = 0
# Verify queue input validation
while queueCode == 0:
    print("Which queue?")
    queue = input()
    queueCode = switch(queue)

api.displayWinrates(api.getMatchList(api.getSummonerId(summonerId),queueCode))
