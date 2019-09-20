import api_request as api
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

# Switch statement for queue type
def switch(queue):
    switcher = {
        'blind': 430,
        'draft': 400,
        'solo': 420,
        'flex': 440,
        'aram': 450
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

fig, ax = plt.subplots()

y_pos = np.arange(len(x))
bar_plot = plt.bar(y_pos, y)
for champion,rect in enumerate(bar_plot):
    if y[champion] > 90:
        height = y[champion] - 5
        color = 'white'
    else:
        height = y[champion] + 0.5
        color = 'black'
    text = str(y[champion]) + "%"
    ax.text(rect.get_x() + rect.get_width()/2., height,
                text,
                ha='center', va='bottom', rotation=0, fontsize='9', color=color)


plt.xlabel('Champion')
plt.ylabel('Winrate')
plt.ylim(0,100)

plt.xticks(y_pos, x, rotation=45, fontsize='10', horizontalalignment='right')


if queue == 'blind' or queue == 'draft':
    queue += ' pick'
else:
    queue = 'ranked ' + queue
title = 'Winrates per champion for ' + summonerId + ' in ' + queue
plt.title(title)
plt.tight_layout()

plt.show()
