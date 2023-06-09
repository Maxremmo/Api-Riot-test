import requests
import time
from dotenv import load_dotenv
load_dotenv()
import os
import pandas as pd
import json

api_key = os.getenv('the_key')  #Development API key for Riot API, expires every 24h

class Summoner:  #Create Class (Account)
    def __init__(self, api_key):
        """User defines class name + puuid function is called and retrieved from account information
            requires an api key as input
        """ 

        self.api_key = api_key
        self.name = input("Enter Account Name: ")
        self.puuid = self.get_puuid()

    def get_puuid(self):
        """Returns puuid needed to get match history"""

        api_url = ("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + self.name) 
        full_url = (api_url + "?api_key=" + self.api_key) 
        resp = requests.get(full_url)
        account_info = resp.json()
        puuid = account_info['puuid']

        return puuid

    def get_match(self, match_iD):
        """Returns  information about one individual match, input is a matchID"""

        my_url = ("https://europe.api.riotgames.com/lol/match/v5/matches/" +
                  match_iD +
                  "?api_key=" + api_key
                  )
        
        match_request = requests.get(my_url)
        match_facts = match_request.json()
        return match_facts
    
    def get_history(self):
        """Returns history of chosen amount of matches
        """

        history_url = (
            "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + 
            self.puuid + 
            "/ids?start=0&count=20" + 
            "&api_key=" + 
            api_key
            )
        
        history_request = requests.get(history_url)
        match_history = history_request.json()
        
        return match_history
    
    def get_participant_index(self, match):
        """ Returns participant index which differs for every game, 
            needed to keep track of only the chosen accounts data
        """

        participant_index = match['metadata']['participants'].index(self.puuid)
    
        return participant_index
    
class Game():
    def __init__(self, match):
        self.match = match
        
        
    def get_kills(self):
        """Returns number of Kills"""

        kills = self.match['info']['participants'][participant_index]['kills']
        
        return kills
    
    def get_deaths(self):
        """Returns number of deaths"""
        
        deaths = self.match['info']['participants'][participant_index]['deaths']
        
        return deaths
    
    def get_assists(self):
        """Returns number of assists"""
        
        assists = self.match['info']['participants'][participant_index]['assists']
        
        return assists
    
    def get_takedowns(self):
        """Returns number of takedowns"""
        
        takedowns = self.match['info']['participants'][participant_index]['challenges']['takedowns']
        
        return takedowns
    
    def get_multikills(self):
        """Returns number of multikills"""
        
        multikills = self.match['info']['participants'][participant_index]['challenges']['multikills']
        
        return multikills
    
    def get_visionScore(self):
        """Returns visionscore"""
        
        visionScore = self.match['info']['participants'][participant_index]['visionScore']
        
        return visionScore

    def get_gameMode (self):
        """Returns game mode"""
        
        mode = self.match['info']['gameMode']

        return mode
    
    def get_championName (self):
        """Returns name of champion played"""
        
        champName = self.match['info']['participants'][participant_index]['championName']

        return champName
    
    def get_role (self):
        """Returns role"""
        
        role = self.match['info']['participants'][participant_index]['individualPosition']

        return role
    
    def get_win (self):
        """ Returns whether the game was won or not"""
        
        won = self.match['info']['participants'][participant_index]['win']

        return won

#initalize account 
active_account = Summoner(api_key)
active_history = active_account.get_history()

#initialize counters (will clean this up)
player_total_kills = 0
player_total_deaths = 0
player_multikills = 0
player_total_takedowns = 0
player_total_vision_score = 0
player_wins = 0
player_losses = 0


current_game = active_account.get_match(active_history[0])

#loop over games, each time getting match data and participant index to track player,
#display Game type, Role, Champion, Kills/Deaths/Assists/ Wins and Loss, Multikills, Takedowns and Vision score
for i in range(len(active_history)):

    current_game = active_account.get_match(active_history[i])

    participant_index = active_account.get_participant_index(current_game)

    active_game = Game(current_game)

    df = current_game['info']['participants'][participant_index]
    
    file_name = f"/Users/maxremme/Desktop/Programming/Code_Academy/Riot/full_games/game_{i}.json"

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(current_game, file, ensure_ascii=False, indent=4)
        
    file_name = f"/Users/maxremme/Desktop/Programming/Code_Academy/Riot/player_stats/game_{i}.json"

    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(df, file, ensure_ascii=False, indent=4)

    player_won = active_game.get_win()
    
    if player_won == True:
        player_wins +=1
        
    else:
        player_losses += 1

    kills = active_game.get_kills()
    player_total_kills = player_total_kills + kills
    deaths = active_game.get_deaths()
    player_total_deaths = player_total_deaths + deaths

    print(
        f"GAME {i} : {active_game.get_gameMode()}\n" 
        f"Role:  {active_game.get_role()}\n"
        f"Champion played: {active_game.get_championName()}\n"
        f"KDA: {active_game.get_kills()}/{active_game.get_deaths()}/{active_game.get_assists()}\n"
        f"Wins : {player_wins}\n"
        f"Losses : {player_losses}\n"
        f"Game won :{active_game.get_win()} \n"
        f"Multikills: {active_game.get_multikills()}\n"
        f"Takedowns: {active_game.get_takedowns()}\n"
        f"Vision Score: {active_game.get_visionScore()}\n"
        f"Takedowns: {active_game.get_takedowns()}\n"
        f"---- ---- ---- ----\n"
)

    time.sleep(0.5)
    
#display match facts over 20 games  
kda = (player_total_kills/player_total_deaths)   
print(
    f"Over 20 Games: \n"  
    f"Total Deaths: {player_total_deaths}\n"  
    f"Total Kills: {player_total_kills}\n"  
    f"KD/A Ratio: {kda}"
)



        




