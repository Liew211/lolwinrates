import api_request as api
import matplotlib.pyplot as plt
import numpy as np
import time


plt.style.use('ggplot')

REGIONS = {
    "br": "br1",
    "eune": "eun1",
    "euw": "euw1",
    "jp": "jp1",
    "kr": "kr",
    "lan": "la1",
    "las": "la2",
    "na": "na1",
    "oce": "oc1",
    "tr": "tr1",
    "ru": "ru"
}

# Queue codes:
# 400 - 5v5 Draft Pick
# 420 - 5v5 Ranked Solo
# 430 - 5v5 Blind Pick
# 440 - 5v5 Ranked Flex
# 450 - 5v5 ARAM
QUEUES = {
    'draft': 400,
    'solo': 420,
    'blind': 430,
    'flex': 440,
    'aram': 450
}


def routingSelector(region):
    """
    Match history data uses routing regions instead
    """
    if region in ["na", "br", "lan", "las", "oce"]:
        return "americas"
    if region in ["kr", "jp"]:
        return "asia"
    if region in ["eune", "euw", "tr", "ru"]:
        return "europe"
    assert False, "not matched"


if __name__ == "__main__":
    # Prompt user for inputs
    region = ""
    while region not in REGIONS:
        print("Region? (i.e. NA)")
        region = input().lower()

    routing = routingSelector(region)
    region = REGIONS[region]

    # Does not verify input for summoner name
    print("Summoner Name?")
    summonerName = input()

    queue = ""
    # Verify queue input validation
    while queue not in QUEUES:
        print("Which queue?")
        queue = input().lower()

    queueCode = QUEUES[queue]

    print("Loading...")

    # Gets start and end time for the function
    start = time.time()

    # Gets list of champions & their winrates as a pair of lists, in order of number of games played
    summonerId = api.getSummonerId(summonerName, region)
    matchlist = api.getMatchList(summonerId, queueCode, routing)
    x, y = api.displayWinrates(summonerId, matchlist, routing)

    end = time.time()
    print(f"Data acquired in {end-start:.2f} seconds.")

    fig, ax = plt.subplots()

    # Plots bar graph
    x_pos = np.arange(len(x))
    bar_plot = plt.bar(x_pos, y)

    # Set bar colors for different winrates
    for i, bar in enumerate(bar_plot):
        if y[i] >= 70:
            bar.set_color("#E19205")
        elif y[i] >= 60 and y[i] < 70:
            bar.set_color("#1F8ECD")
        elif y[i] >= 50 and y[i] < 60:
            bar.set_color("#2DAF7F")
        else:
            bar.set_color("grey")

    # Creates labels for each bar
    for champion, rect in enumerate(bar_plot):
        # Label in white, inside the bar if the winrate is greater than 90%
        if y[champion] > 90:
            height = y[champion] - 5
            color = 'white'
        else:
            height = y[champion] + 0.5
            color = 'black'
        text = f"{y[champion]}%"
        ax.text(
            rect.get_x() + rect.get_width()/2., height, text,
            ha='center', va='bottom', rotation=0, fontsize='9', color=color
        )

    # X and Y axis labels
    plt.xlabel('Champion')
    plt.ylabel('Winrate')
    plt.ylim(0, 100)

    # Rotated X axis label for each champion
    plt.xticks(
        x_pos, x,
        rotation=45, fontsize='10', horizontalalignment='right'
    )

    # Displays title
    if queue == 'blind' or queue == 'draft':
        queue += ' pick'
    else:
        queue = 'ranked ' + queue
    title = f'Winrates per champion for {summonerName} in {queue}'
    plt.title(title)

    # Prevent labels from being cut off
    plt.tight_layout()
    plt.show()
