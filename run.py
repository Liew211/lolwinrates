import api_request as api
import matplotlib.pyplot as plt
import numpy as np
import time
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
# Does not verify input for summoner name
print("Summoner Name?")
summonerId = input()

queueCode = 0
# Verify queue input validation
while queueCode == 0:
    print("Which queue?")
    queue = input().lower()
    queueCode = switch(queue)

print("Loading information from the nickname...")

# Gets start and end time for the function
start = time.time()
# Gets list of champions & their winrates as a pair of lists, in order of number of games played
x, y = api.displayWinrates(api.getMatchList(api.getSummonerId(summonerId),queueCode))

end = time.time()
print(f"Data acquired in {end-start:.2f} seconds.")

fig, ax = plt.subplots()

# Plots bar graph
x_pos = np.arange(len(x))
bar_plot = plt.bar(x_pos, y)

# Set bar colours for different winrates
for i, bar in enumerate(bar_plot):
    if y[i]>=70:
        bar.set_color("#FFAB0F")
    elif y[i]>=60 and y[i]<70:
        bar.set_color("#006AB7")
    elif y[i]>=50 and y[i]<60:
        bar.set_color("#80C1F0")
    else:
        bar.set_color("grey")

# Creates labels for each bar
for champion,rect in enumerate(bar_plot):
    # Label in white, inside the bar if the winrate is greater than 90%
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

# X and Y axis labels
plt.xlabel('Champion')
plt.ylabel('Winrate')
plt.ylim(0,100)

# Rotated X axis label for each champion
plt.xticks(x_pos, x, rotation=45, fontsize='10', horizontalalignment='right')

# Displays title
if queue == 'blind' or queue == 'draft':
    queue += ' pick'
else:
    queue = 'ranked ' + queue
title = 'Winrates per champion for ' + summonerId + ' in ' + queue
plt.title(title)

# Prevent labels from being cut off
plt.tight_layout()
plt.show()
