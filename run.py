import api_request as api
import matplotlib.pyplot as plt
import numpy as np

# Switch statement for queue type
def switch(queue):
    switcher = {
        'blind': 430,
        'draft': 400,
        'solo': 420,
        'flex': 440,
    }
    return switcher.get(queue, 0)

# Prompt user for inputs
print("Summoner Name?")
summonerId = input()

queueCode = 0
# Verify queue input validation
while queueCode == 0:
    print("Which queue?")
    queue = input().lower()
    queueCode = switch(queue)

x, y = api.displayWinrates(api.getMatchList(api.getSummonerId(summonerId),queueCode))

y_pos = np.arange(len(x))
plt.bar(y_pos, y)
plt.xlabel('Champion')
plt.ylabel('Winrate')
plt.ylim(0,100)

plt.xticks(y_pos, x, rotation=30, fontsize='10', horizontalalignment='right')


if queue == 'blind' or queue == 'draft':
    queue += ' pick'
else:
    queue = 'ranked ' + queue
title = 'Winrates per champion for ' + summonerId + ' in ' + queue
plt.title(title)
plt.tight_layout()
plt.show()
