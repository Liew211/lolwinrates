# lolwinrates

I created this project for some practice with Python and APIs.  The [Riot Games API](https://developer.riotgames.com) can be accessed by signing in with your League of Legends account, where you can get your 24-hour developer API key.

To use this program, run `run.py`.  You'll be prompted to enter the summoner name (not case sensitive), and the queue type: "blind", "draft", "solo", or "flex".  The script will access your match history, and parse through up to 50 of your past games in that queue, then display your win-loss record and win percentage, then the list of champions you played, the winrates of each champion, and number of games played for each champion, all sorted by the number of games.
