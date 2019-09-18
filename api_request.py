import requests

# development key changes every 24 hours, access it by logging in 
api_key = "RGAPI-c81275da-997c-413f-ab07-4dd4fcc6f722"

# request headers
headers = {
    "Origin": "https://developer.riotgames.com",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Riot-Token": api_key,
    "Accept-Language": "en-us",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15"
}

# get latest version
version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]

# convert key to champion name
datadragon = requests.get('http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(version)).json()
champions = {}
for champion in datadragon["data"]:
    key = int(datadragon["data"][champion]["key"])
    champions[key] = champion

def championId_to_name(id: int):
    return champions[id]

# Given a list of wins and losses, calculate the winrate as a percentage
def winrate(winloss: list):
    return winloss[0] / (winloss[0] + winloss[1]) * 100

# Each player has an encrypted account ID that is used to get match history and other data
def getSummonerId(summonerName: str):
    summonerNameUrl = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + summonerName
    response = requests.get(summonerNameUrl, headers = headers).json()
    return response['accountId']

# List of past matches from the player in a certain queue
# Queue codes:
# 400 - 5v5 Draft Pick
# 420 - 5v5 Ranked Solo
# 430 - 5v5 Blind Pick
# 440 - 5v5 Ranked Flex
# 450 - 5v5 ARAM
def getMatchList(summonerId: str, queue: int):
    params = '?queue={}&season=13&endIndex=50'.format(queue)
    summonerMatchlistUrl = 'https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + summonerId + params
    return requests.get(summonerMatchlistUrl, headers = headers).json()

# Given matchlist, print the overall winrate and the list of champions played, their winrates, and number of games played
def displayWinrates(matchList: dict):
    win_loss = [0,0]
    champion_winrates = {}

    # Parse through matchlist
    for match in matchList['matches']:
        champion = championId_to_name(match['champion'])
        gameId = match['gameId']

        # Access match data
        matchUrl = 'https://na1.api.riotgames.com/lol/match/v4/matches/{}'.format(gameId)
        matchInfo = requests.get(matchUrl, headers = headers).json()
        
        # Find participant ID
        participantId = 0
        for player in matchInfo['participantIdentities']:
            if player['player']['summonerName'] == 'Liew211':
                participantId = player['participantId']
        
        # Use participant ID to determine which team player is on
        if participantId <= 5:
            participantId = 0
        else:
            participantId = 1
        
        # Increments win/loss counters for overall and per champion
        if matchInfo['teams'][participantId]['win'] == 'Win':
            win_loss[0] += 1
            if champion in champion_winrates:
                champion_winrates[champion][0] += 1
            else:
                champion_winrates[champion] = [1,0,0]
        else:
            win_loss[1] += 1
            if champion in champion_winrates:
                champion_winrates[champion][1] += 1
            else:
                champion_winrates[champion] = [0,1,0]
        champion_winrates[champion][2] += 1


    # Sort champions in descending order of games 
    champion_winrates = dict(sorted(champion_winrates.items(), reverse=True, key=lambda x: x[1][2]))

    # Overall wins and losses
    print(win_loss[0], 'wins', win_loss[1], 'losses')

    # Overall winrate to two decimal places
    print('%.2f'%(winrate(win_loss)) + "%")
    for champion in champion_winrates:
        # Prints champion winrates and checks for plural games
        games = champion_winrates[champion][0] + champion_winrates[champion][1]
        if games == 1:
            print(champion, '%.2f'%(winrate(champion_winrates[champion])) + '%', champion_winrates[champion][2], 'game')
        else:
            print(champion, '%.2f'%(winrate(champion_winrates[champion])) + '%', champion_winrates[champion][2], 'games')
