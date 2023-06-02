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

       
#initalize account 
active_account = Summoner(api_key)

active_history = active_account.get_history()

print(active_history)


#initialize counters (will clean this up)

player1_total_kills = 0
    
player1_total_deaths = 0
    
player1_multikills = 0
    
player1_total_takedowns = 0
    
player1_total_vision_score = 0
    
player1_wins = 0
    
player1_losses = 0

#loop over games, each time getting match data and participant index to track player,
#display Game type, Role, Champion, Kills/Deaths/Assists/ Wins and Loss, Multikills, Takedowns and Vision score
for i in range(len(active_history)):
        
    current_game = active_account.get_match(active_history[i])
    
    participant_index = active_account.get_participant_index(current_game)
    
    print("GAME " + str(i) + ":" + "\n" + "Game Type: " + current_game['info']['gameMode'])
    
    print("Role: " + current_game['info']['participants'][participant_index]['individualPosition'])
    
    player1_champion = current_game['info']['participants'][participant_index]['championName']

    print("Champion played: " + current_game['info']['participants'][participant_index]['championName'])

    print(
        "KDA: " + str(current_game['info']['participants'][participant_index]['kills']) + "/" +

        str(current_game['info']['participants'][participant_index]['deaths']) + "/" +

        str(current_game['info']['participants'][participant_index]['assists'])
        
          
          )
    
    player1_won = current_game['info']['participants'][participant_index]['win']
    
    
    if player1_won == True:
        
        player1_wins +=1
        
    elif player1_won == False:
        
        player1_losses += 1
    
    print(f"Wins : {player1_wins}")
    
    print(f"Wins : {player1_losses}")
    
    print("Game won: " + str(current_game['info']['participants'][participant_index]['win']))
    
    player1_kills = current_game['info']['participants'][participant_index]['kills']
    
    player1_total_kills = player1_total_kills + player1_kills
    
    player1_deaths = current_game['info']['participants'][participant_index]['deaths']
    
    player1_total_deaths = player1_total_deaths + player1_deaths
    
    player1_multikills = str(current_game['info']['participants'][participant_index]['challenges']['multikills'])
    
    print("Multikills: " + str(current_game['info']['participants'][participant_index]['challenges']['multikills']))
    
    player1_takedowns = str(current_game['info']['participants'][participant_index]['challenges']['takedowns'])
    
    print("Takedowns: " + str(current_game['info']['participants'][participant_index]['challenges']['takedowns']))
    
    player1_vision_score = str(current_game['info']['participants'][participant_index]['visionScore'])
    
    print("Vision Score: " + str(current_game['info']['participants'][participant_index]['visionScore']) + "\n")

    print("---- ---- ---- ----\n")

    time.sleep(1)

#display match facts over 20 games     
print( "Over 20 games: \n" + 
    "Total Kills: " + str(player1_total_kills) +
      
      "\nTotal Deaths: " + str(player1_total_deaths) +
      
      "\nK/D Ratio: " + str(player1_total_kills/player1_total_deaths)





)


