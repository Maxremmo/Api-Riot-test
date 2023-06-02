import requests
import time
from dotenv import load_dotenv
load_dotenv()
import os

#Development API key for Riot API, expires every 24h
api_key = os.getenv('the_key')

#Create Class (Account)
class Summoner:

    #User defines class name + puuid function is called and retrieved from account information
    def __init__(self, api_key):
        self.api_key = api_key
        self.name = input("Enter Account Name: ")
        self.puuid = self.get_puuid()

        
    #puuid needed to get match history 
    def get_puuid(self):
        api_url = ("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + self.name) 
        full_url = (
        api_url + "?api_key=" + self.api_key
           
             ) 
        resp = requests.get(full_url)

        account_info = resp.json()

        puuid = account_info['puuid']

        return puuid

    #get all information about one individual match
    def get_match(self, match_iD):
        my_url = ("https://europe.api.riotgames.com/lol/match/v5/matches/" +
                  
                  match_iD +

                  "?api_key=" + api_key)
        
        match_request = requests.get(my_url)
        match_facts = match_request.json()
        return match_facts
    
    #get history of chosen amount of matches
    def get_history(self):
        history_url = ("https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + 
                  self.puuid + 
                  "/ids?start=0&count=20" + 
                  "&api_key=" + 
                  api_key
                  )
        
        history_request = requests.get(history_url)
        match_history = history_request.json()
        return match_history
    
    #participant index differs for every game, needed to keep track of only the chosen accounts data
    def get_participant_index(self, match):

        participant_index = match['metadata']['participants'].index(self.puuid)
    
        return participant_index
    
class Game():

    def __init__(self, match):
        self.match = match
        
        
    def get_kills(self):

        kills = self.match['info']['participants'][participant_index]['kills']
        
        return kills
    
    def get_deaths(self):
        
        deaths = self.match['info']['participants'][participant_index]['deaths']
        
        return deaths
    
    def get_assists(self):
        
        assists = self.match['info']['participants'][participant_index]['assists']
        
        return assists
    
    def get_takedowns(self):
        
        takedowns = self.match['info']['participants'][participant_index]['challenges']['takedowns']
        
        return takedowns
    
    def get_multikills(self):
        
        multikills = self.match['info']['participants'][participant_index]['challenges']['multikills']
        
        return multikills
    
    def get_visionScore(self):
        
        visionScore = self.match['info']['participants'][participant_index]['visionScore']
        
        return visionScore

    def get_gameMode (self):
        
        mode = self.match['info']['gameMode']

        return mode
    
    def get_championName (self):
        
        champName = self.match['info']['participants'][participant_index]['championName']

        return champName
    
    def get_role (self):
        
        role = self.match['info']['participants'][participant_index]['individualPosition']

        return role
    
    def get_win (self):
        
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

#loop over games, each time getting match data and participant index to track player,
#display Game type, Role, Champion, Kills/Deaths/Assists/ Wins and Loss, Multikills, Takedowns and Vision score
for i in range(len(active_history)):

    current_game = active_account.get_match(active_history[i])

    participant_index = active_account.get_participant_index(current_game)

    active_game = Game(current_game)
    
    print(f"GAME {i} : {active_game.get_gameMode()}")
    
    print(f"Role:  {active_game.get_role()}")

    print(f"Champion played: {active_game.get_championName()}")

    print(f"KDA: {active_game.get_kills()}/{active_game.get_deaths()}/{active_game.get_assists()}")
    
    player_won = active_game.get_win()
    
    if player_won == True:
        player_wins +=1
        
    else:
        player_losses += 1
    
    print(f"Wins : {player_wins}")
    
    print(f"Losses : {player_losses}")
    
    print(f"Game won:{active_game.get_win()} ")
    
    kills = active_game.get_kills()
    
    player_total_kills = player_total_kills + kills
    
    deaths = active_game.get_deaths()
    
    player_total_deaths = player_total_deaths + deaths
    
    multikills = active_game.get_multikills()
    
    print(f"Multikills: {active_game.get_multikills()}" )
    
    takedowns = active_game.get_takedowns()

    print(f"Takedowns: {active_game.get_takedowns()}" )
    
    vision_score = active_game.get_visionScore()
    
    print(f"Vision Score: {active_game.get_visionScore()} " )

    print("---- ---- ---- ----\n")

    time.sleep(1)
#display match facts over 20 games  
kda = (player_total_kills/player_total_deaths)   
print( f"Over 20 Games: \n  Total Deaths: {player_total_deaths}\n  Total Kills: {player_total_kills}\n  KD/A Ratio: {kda}"
)


