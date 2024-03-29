import requests
import time
from dotenv import load_dotenv
import os
import pandas as pd
import json
import datetime as dt

load_dotenv()
API_KEY = os.getenv("MY_API")  # Development API key for Riot API, expires every 24h


class Summoner:
    BASE_URL = "https://euw1.api.riotgames.com/lol/"

    def __init__(
        self,
        name,
        api_key=API_KEY,
    ):
        """User defines class name + puuid function is called and retrieved from account information
        requires an api key as input
        """

        self.api_key = api_key
        self.name = name
        self.puuid = self.get_puuid()
        self.participant_index = ""
        self.summoner_id = self.get_summoner_id()

    def get_puuid(self):
        """Returns puuid needed to get match history"""

        api_url = f"{self.BASE_URL}summoner/v4/summoners/by-name/{self.name}?api_key={self.api_key}"

        resp = requests.get(api_url)
        account_info = resp.json()
        puuid = account_info["puuid"]

        return puuid

    def get_summoner_id(self):
        """Returns Summoner ID"""
        api_url = f"{self.BASE_URL}summoner/v4/summoners/by-name/{self.name}?api_key={self.api_key}"
        resp = requests.get(api_url)
        account_info = resp.json()
        summoner_id = account_info["id"]
        return summoner_id

    def live_game(self):
        api_url = f"https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{self.summoner_id}?apikey={self.api_key}"
        resp = requests.get(api_url)
        live_game = resp.json()

        return live_game

    def get_match(self, match_iD):
        """Returns  information about one individual match, input is a matchID"""

        my_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_iD}?api_key={self.api_key}"

        match_request = requests.get(my_url)
        match_facts = match_request.json()

        return match_facts

    def get_history(self):
        """Returns history of chosen amount of matches"""

        history_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count=20&api_key={self.api_key}"

        history_request = requests.get(history_url)
        match_history = history_request.json()

        return match_history

    def get_participant_index(self, match):
        """Returns participant index which differs for every game,
        needed to keep track of only the chosen accounts data
        """

        participant_index = match["metadata"]["participants"].index(self.puuid)

        self.participant_index = participant_index

        return participant_index


class Game:
    def __init__(self, match):
        self.match = match
        self.partindex = ""

    def set_partindex(self, part_index):
        part_index = part_index
        self.partindex = part_index

    def get_kills(self):
        """Returns number of Kills"""

        kills = self.match["info"]["participants"][self.partindex]["kills"]

        return kills

    def get_deaths(self):
        """Returns number of deaths"""

        deaths = self.match["info"]["participants"][self.partindex]["deaths"]

        return deaths

    def get_assists(self):
        """Returns number of assists"""

        assists = self.match["info"]["participants"][self.partindex]["assists"]

        return assists

    def get_takedowns(self):
        """Returns number of takedowns"""

        takedowns = self.match["info"]["participants"][self.partindex]["challenges"][
            "takedowns"
        ]

        return takedowns

    def get_multikills(self):
        """Returns number of multikills"""

        multikills = self.match["info"]["participants"][self.partindex]["challenges"][
            "multikills"
        ]

        return multikills

    def get_visionScore(self):
        """Returns visionscore"""

        visionScore = self.match["info"]["participants"][self.partindex]["visionScore"]

        return visionScore

    def get_gameMode(self):
        """Returns game mode"""

        mode = self.match["info"]["gameMode"]

        return mode

    def get_championName(self):
        """Returns name of champion played"""

        champName = self.match["info"]["participants"][self.partindex]["championName"]

        return champName

    def get_role(self):
        """Returns role"""

        role = self.match["info"]["participants"][self.partindex]["individualPosition"]

        return role

    def get_win(self):
        """Returns whether the game was won or not"""

        won = self.match["info"]["participants"][self.partindex]["win"]

        return won


# active_account = Summoner("Joeee Biden")
# active_history = active_account.get_history()
# current_game = active_account.get_match(active_history[0])


def stats_to_df(
    usernames=[
        "GOD EZREAL",
        "Borrzz",
        "TPancakeBoy",
        "Hakuuna",
        "bad name",
        "Greystonup",
        "jennerkris",
        "Winie puh",
    ]
):
    for name in usernames:
        try:
            # initalize accounts
            active_account = Summoner(name)
            active_history = active_account.get_history()

            list_dfs = []
            for i in range(len(active_history)):
                current_game = active_account.get_match(active_history[i])
                participant_index = active_account.get_participant_index(current_game)
                active_game = Game(current_game)
                active_game.set_partindex(participant_index)
                df = current_game["info"]["participants"][participant_index]
                df["game_id"] = current_game["metadata"]["matchId"]
                df["gameStartTimestamp"] = current_game["info"]["gameStartTimestamp"]
                df["gameEndTimestamp"] = current_game["info"]["gameEndTimestamp"]
                df_file = pd.json_normalize(df)
                list_dfs.append(df_file)

            my_df = pd.concat(list_dfs)
            the_df = my_df.copy()
            final_df = the_df[
                [
                    "game_id",
                    "allInPings",
                    "assistMePings",
                    "assists",
                    "baitPings",
                    "baronKills",
                    "champExperience",
                    "champLevel",
                    "championName",
                    "damageDealtToObjectives",
                    "damageDealtToTurrets",
                    "damageSelfMitigated",
                    "deaths",
                    "doubleKills",
                    "dragonKills",
                    "firstBloodAssist",
                    "firstBloodKill",
                    "gameEndedInSurrender",
                    "goldEarned",
                    "goldSpent",
                    "individualPosition",
                    "item0",
                    "item1",
                    "item2",
                    "item3",
                    "item4",
                    "item5",
                    "item6",
                    "itemsPurchased",
                    "killingSprees",
                    "kills",
                    "lane",
                    "largestKillingSpree",
                    "largestMultiKill",
                    "longestTimeSpentLiving",
                    "magicDamageDealt",
                    "magicDamageDealtToChampions",
                    "magicDamageTaken",
                    "needVisionPings",
                    "neutralMinionsKilled",
                    "nexusKills",
                    "nexusLost",
                    "nexusTakedowns",
                    "objectivesStolen",
                    "participantId",
                    "pentaKills",
                    "physicalDamageDealt",
                    "physicalDamageDealtToChampions",
                    "physicalDamageTaken",
                    "quadraKills",
                    "spell1Casts",
                    "spell2Casts",
                    "spell3Casts",
                    "spell4Casts",
                    "summoner1Casts",
                    "summoner1Id",
                    "summoner2Casts",
                    "summoner2Id",
                    "summonerId",
                    "summonerLevel",
                    "summonerName",
                    "teamEarlySurrendered",
                    "teamId",
                    "teamPosition",
                    "timeCCingOthers",
                    "timePlayed",
                    "totalAllyJungleMinionsKilled",
                    "totalDamageDealt",
                    "totalDamageDealtToChampions",
                    "totalDamageShieldedOnTeammates",
                    "totalDamageTaken",
                    "totalEnemyJungleMinionsKilled",
                    "totalHeal",
                    "totalHealsOnTeammates",
                    "totalMinionsKilled",
                    "totalTimeCCDealt",
                    "totalTimeSpentDead",
                    "totalUnitsHealed",
                    "tripleKills",
                    "trueDamageDealt",
                    "trueDamageDealtToChampions",
                    "trueDamageTaken",
                    "turretKills",
                    "turretTakedowns",
                    "turretsLost",
                    "unrealKills",
                    "visionClearedPings",
                    "visionScore",
                    "visionWardsBoughtInGame",
                    "wardsKilled",
                    "wardsPlaced",
                    "win",
                    "gameStartTimestamp",
                    "gameEndTimestamp",
                    "challenges.abilityUses",
                    "challenges.acesBefore15Minutes",
                    "challenges.alliedJungleMonsterKills",
                    "challenges.baronTakedowns",
                    "challenges.bountyGold",
                    "challenges.buffsStolen",
                    "challenges.completeSupportQuestInTime",
                    "challenges.controlWardsPlaced",
                    "challenges.damagePerMinute",
                    "challenges.damageTakenOnTeamPercentage",
                    "challenges.dancedWithRiftHerald",
                    "challenges.deathsByEnemyChamps",
                    "challenges.dodgeSkillShotsSmallWindow",
                    "challenges.doubleAces",
                    "challenges.dragonTakedowns",
                    "challenges.earlyLaningPhaseGoldExpAdvantage",
                    "challenges.elderDragonKillsWithOpposingSoul",
                    "challenges.elderDragonMultikills",
                    "challenges.enemyChampionImmobilizations",
                    "challenges.enemyJungleMonsterKills",
                    "challenges.epicMonsterKillsNearEnemyJungler",
                    "challenges.epicMonsterKillsWithin30SecondsOfSpawn",
                    "challenges.epicMonsterSteals",
                    "challenges.epicMonsterStolenWithoutSmite",
                    "challenges.firstTurretKilled",
                    "challenges.firstTurretKilledTime",
                    "challenges.flawlessAces",
                    "challenges.fullTeamTakedown",
                    "challenges.gameLength",
                    "challenges.goldPerMinute",
                    "challenges.hadOpenNexus",
                    "challenges.immobilizeAndKillWithAlly",
                    "challenges.initialBuffCount",
                    "challenges.initialCrabCount",
                    "challenges.jungleCsBefore10Minutes",
                    "challenges.kTurretsDestroyedBeforePlatesFall",
                    "challenges.kda",
                    "challenges.killAfterHiddenWithAlly",
                    "challenges.killParticipation",
                    "challenges.killedChampTookFullTeamDamageSurvived",
                    "challenges.killsNearEnemyTurret",
                    "challenges.killsUnderOwnTurret",
                    "challenges.killsWithHelpFromEpicMonster",
                    "challenges.knockEnemyIntoTeamAndKill",
                    "challenges.landSkillShotsEarlyGame",
                    "challenges.laneMinionsFirst10Minutes",
                    "challenges.laningPhaseGoldExpAdvantage",
                    "challenges.legendaryCount",
                    "challenges.lostAnInhibitor",
                    "challenges.maxLevelLeadLaneOpponent",
                    "challenges.mejaisFullStackInTime",
                    "challenges.moreEnemyJungleThanOpponent",
                    "challenges.multikills",
                    "challenges.multikillsAfterAggressiveFlash",
                    "challenges.outerTurretExecutesBefore10Minutes",
                    "challenges.outnumberedKills",
                    "challenges.outnumberedNexusKill",
                    "challenges.perfectGame",
                    "challenges.pickKillWithAlly",
                    "challenges.quickCleanse",
                    "challenges.quickFirstTurret",
                    "challenges.quickSoloKills",
                    "challenges.riftHeraldTakedowns",
                    "challenges.saveAllyFromDeath",
                    "challenges.scuttleCrabKills",
                    "challenges.skillshotsDodged",
                    "challenges.skillshotsHit",
                    "challenges.snowballsHit",
                    "challenges.soloBaronKills",
                    "challenges.soloKills",
                    "challenges.stealthWardsPlaced",
                    "challenges.survivedSingleDigitHpCount",
                    "challenges.survivedThreeImmobilizesInFight",
                    "challenges.takedownOnFirstTurret",
                    "challenges.takedowns",
                    "challenges.takedownsFirstXMinutes",
                    "challenges.takedownsInEnemyFountain",
                    "challenges.teamBaronKills",
                    "challenges.teamDamagePercentage",
                    "challenges.teamElderDragonKills",
                    "challenges.teamRiftHeraldKills",
                    "challenges.tookLargeDamageSurvived",
                    "challenges.turretPlatesTaken",
                    "challenges.turretsTakenWithRiftHerald",
                    "challenges.visionScorePerMinute",
                    "challenges.wardTakedowns",
                ]
            ]
            if name != usernames[-1]:
                time.sleep(1)

            save_name = f"data/games.csv"

            try:
                existing_df = pd.read_csv(save_name)
                # Concatenate the existing data with the new data
                final_df = pd.concat([existing_df, final_df])
            except FileNotFoundError:
                # If the file doesn't exist, no need to concatenate, just use very_final_df
                pass

            final_df.to_csv(save_name, index=False)

        except Exception as e:
            print(f"An error occurred for {name}: {e}")
            print(f"Skipping {name}")

            # Skip to the next user if an error occurs
            continue


def run_stats(username):
    # initalize account
    active_account = Summoner(username)
    active_history = active_account.get_history()

    # initialize counters (will clean this up)
    player_total_kills = 0
    player_total_deaths = 0
    player_multikills = 0
    player_total_takedowns = 0
    player_total_vision_score = 0
    player_wins = 0
    player_losses = 0

    # loop over games, each time getting match data and participant index to track player,
    # display Game type, Role, Champion, Kills/Deaths/Assists/ Wins and Loss, Multikills, Takedowns and Vision score

    for i in range(len(active_history)):
        current_game = active_account.get_match(active_history[i])

        participant_index = active_account.get_participant_index(current_game)

        active_game = Game(current_game)

        active_game.set_partindex(participant_index)

        df = current_game["info"]["participants"][participant_index]

        file_name = f"/Users/maxremme/Desktop/Programming/Code_Academy/Riot/full_games/game_{i}.json"

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(current_game, file, ensure_ascii=False, indent=4)

        file_name = f"/Users/maxremme/Desktop/Programming/Code_Academy/Riot/player_stats/game_{i}.json"

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(df, file, ensure_ascii=False, indent=4)

        player_won = active_game.get_win()

        if player_won == True:
            player_wins += 1

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

    # display match facts over 20 games
    kda = player_total_kills / player_total_deaths
    print(
        f"Over 20 Games: \n"
        f"Total Deaths: {player_total_deaths}\n"
        f"Total Kills: {player_total_kills}\n"
        f"KD/A Ratio: {kda}"
    )


# run_stats()
stats_to_df()
