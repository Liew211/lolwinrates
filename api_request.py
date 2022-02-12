import configparser
import requests

# Development key changes every 24 hours, access it by logging in to the Riot Developer Portal with your League of Legends account
config = configparser.ConfigParser()
config.read('config.cfg')
api_key = config["AUTH"]["RIOT_API_KEY"]

# request headers
headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": api_key,
    "Accept-Language": "en-us",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
}


def winrate(wins, losses):
    """
    Given number of wins and losses, calculate the winrate as a percentage
    """
    return wins / (wins + losses) * 100


def getSummonerId(summonerName: str, region):
    """
    Each player has an encrypted account ID that is used to get match history and other data
    """
    summonerNameUrl = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}'
    response = requests.get(summonerNameUrl, headers=headers)
    if not response.ok:
        print(response.json()['status']['message'])
        exit()
    return response.json()['puuid']


def getMatchList(summonerId: str, queue: int, routing):
    params = f'?queue={queue}&count=5'
    summonerMatchlistUrl = f'https://{routing}.api.riotgames.com/lol/match/v5/matches/by-puuid/{summonerId}/ids{params}'
    res = requests.get(summonerMatchlistUrl, headers=headers).json()
    return res


def displayWinrates(summonerId, matchList: list, routing):
    """
    Iterates through matchlist, prints out results and returns list of
    champions played, and a list of their corresponding winrates
    """
    wins, losses = (0, 0)
    champion_winrates = {}

    # Parse through matchlist
    for matchId in matchList:

        # Access match data
        matchUrl = f'https://{routing}.api.riotgames.com/lol/match/v5/matches/{matchId}'
        matchInfo = requests.get(matchUrl, headers=headers).json()["info"]

        for player in matchInfo["participants"]:
            if player["puuid"] == summonerId:
                win = player["win"]
                champion = player["championName"]
                break

        # Increments win/loss counters for overall and per champion
        if win:
            wins += 1
            if champion in champion_winrates:
                champion_winrates[champion][0] += 1
            else:
                champion_winrates[champion] = [1, 0, 0]
        else:
            losses += 1
            if champion in champion_winrates:
                champion_winrates[champion][1] += 1
            else:
                champion_winrates[champion] = [0, 1, 0]
        champion_winrates[champion][2] += 1

    # Sort champions in descending order of games
    champion_winrates = dict(
        sorted(champion_winrates.items(), reverse=True, key=lambda x: x[1][2]))
    champion_list = []
    champion_winrates_list = []

    # Overall wins and losses
    print(wins, 'wins', losses, 'losses')

    # Overall winrate to two decimal places
    print('%.2f' % (winrate(wins, losses)) + "%")
    for champion in champion_winrates:
        # Prints champion winrates and checks for plural games
        percentage = '%.2f' % (winrate(champion_winrates[champion]))
        games = champion_winrates[champion][2]

        champion_list.append(champion)
        champion_winrates_list.append(float(percentage))

        if games == 1:
            print(champion, percentage + '%', games, 'game')
        else:
            print(champion, percentage + '%', games, 'games')

    return champion_list, champion_winrates_list
