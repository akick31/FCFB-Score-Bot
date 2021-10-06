import praw
import discord
import json
import datetime
from discord.ext import commands
from name_fix import handleNamingInconsistincies
from name_fix import changeUserInputTeams
from vegas_odds import getVegasOdds
from color import getTeamColors
from game_data import parse_quarter
from game_data import parse_yard_line
from game_data import parse_down
from game_data import parse_possession
from game_data import parse_time
from game_data import parse_home_score
from game_data import parse_away_score
from game_data import parse_home_team
from game_data import parse_away_team
from game_data import parse_home_user
from game_data import parse_away_user
from game_data import parse_waiting_on
from game_thread_data import searchForGameThread
from game_thread_data import searchForTeamGameThread
from game_thread_data import saveGithubData
from gist_data import iterate_through_game_gist
from thread_crawler import threadCrawler
from win_probability import get_in_game_win_probability
from sheets_functions import getStandingsData
from sheets_functions import getRankingsData

"""
Handle the Discord side of the bot. Look for messages and post responses

@author: apkick
"""
 
"""
Parse what season the user is looking for, so that the bot knows which date 
range to look at. Also parse if the user is looking for a postseason game

"""
def parse_season(away_team):
    postseason = 0
    season = "S6"
    if(("S1" in away_team or "S2" in away_team or "S3" in away_team or "S4" in away_team or "S5" in away_team or "S6" in away_team)
           or ("s1" in away_team or "s2" in away_team or "s3" in away_team or "s4" in away_team or "s5" in away_team or "s6" in away_team)):
        teamSplit = away_team.split(" ")
        i = 0
        for split in teamSplit:
            if(("S1" in split or "S2" in split or "S3" in split or "S4" in split or "S5" in split or "S6" in split)
               or ("s1" in split or "s2" in split or "s3" in split or "s4" in split or "s5" in split or "s6" in split)):
                season = teamSplit[i]
            if("postseason" in split or "Postseason" in split):
                postseason = 1
            i = i + 1
        away_team = away_team.split(season)[0] 
        away_team = away_team.strip()
    return {1: away_team, 2: season, 3: postseason}

"""
Make posts for ongoing games on Reddit

"""
async def make_ongoing_game_post(message, submission, curClock, cur_down, cur_possession, cur_yard_line, vegasOdds, team, opponentTeam, score, opponentScore, cur_win_probability, waiting_on):
    odds = round(vegasOdds * 2) / 2
    if(odds == 0):
        odds = "Push"
    elif(odds > 0):
        odds = "+" + str(odds)
    post = "**" + curClock +  " | " + opponentTeam + " " + opponentScore + " " + team + " " + score + " (" + str(odds) + ")** \n"
    yardPost = cur_down + " | :football: " + cur_possession + " | " + cur_yard_line + "\n"
    winPost = "Each team has a 50% chance to win\n"
    if(int(cur_win_probability) >= 50):
        winPost = team + " has a " + str(int(cur_win_probability)) + "% chance to win\n"
    elif(int(cur_win_probability) < 50):
        winPost = opponentTeam + " has a " + str(100-int(cur_win_probability)) + "% chance to win\n"
    waiting_onPost = "Waiting on " + waiting_on + " for a number\n"
    await message.channel.send(post + yardPost + winPost + waiting_onPost + submission.url + "\n")

"""
Get information to make a post for ongoing games on Reddit

"""
async def get_ongoing_game_information(message, submission, home_vegas_odds, away_vegas_odds, home_team, away_team, home_score, away_score):
    # Get win probability
    cur_possession = parse_possession(submission.selftext)
    offense_win_probability = get_in_game_win_probability(home_team, away_team)
    print(offense_win_probability)
    if(cur_possession == home_team):
        home_win_probability = offense_win_probability
    else:
        home_win_probability = 100-offense_win_probability
    away_win_probability = 100-home_win_probability
    
    # Get other game data
    cur_yard_line = parse_yard_line(submission.selftext)
    cur_quarter = parse_quarter(submission.selftext)
    cur_down = parse_down(submission.selftext)
    cur_time = parse_time(submission.selftext)
    home_user = parse_home_user(submission.selftext)
    away_user = parse_away_user(submission.selftext)
    waiting_on = parse_waiting_on(submission.selftext, home_user, away_user, home_team, away_team)
    # If game is final, display that
    if(cur_quarter == "OT"):
        curClock = "OT"
    else:
        curClock = str(cur_time) + " " + str(cur_quarter) 
    # If home team is winning or the score is tied
    if(int(home_score) > int(away_score) or int(home_score) == int(away_score)):
        await make_ongoing_game_post(message, submission, curClock, cur_down, cur_possession, cur_yard_line, home_vegas_odds, home_team, away_team, home_score, away_score, home_win_probability, waiting_on)
    #If the home team is losing
    elif(int(home_score) < int(away_score)):
        await make_ongoing_game_post(message, submission, curClock, cur_down, cur_possession, cur_yard_line, away_vegas_odds, away_team, home_team, away_score, home_score, away_win_probability, waiting_on)

"""
Make posts for games that went final on Reddit

"""
async def make_game_final_score_post(message, submission, team, opponentTeam, vegasOdds, score, opponentScore):
    odds = round(vegasOdds * 2) / 2
    numberOdds = odds
    if(odds == 0):
        odds = "Push"
    elif(odds > 0):
        odds = "+" + str(odds)
    post = "**FINAL | " + team + " defeated " + opponentTeam + " " + score + "-" + opponentScore + "**\n"
    if(int(numberOdds) > 0):
        await message.channel.send(post + "UPSET! " + team + " was underdogs at " + str(odds) + " and won!")
    if(int(numberOdds) < 0 and ((int(opponentScore) - int(score)) > numberOdds)):
        await message.channel.send(post + opponentTeam + " beat the spread listed at " + str(odds))
    elif(int(numberOdds) < 0 and ((int(opponentScore) - int(score)) < numberOdds)):
        print(numberOdds)
        await message.channel.send(post + team + " covered the spread listed at " + str(odds))
    if(int(numberOdds) == 0 or ((int(opponentScore) - int(score)) == numberOdds)):
        await message.channel.send(post + "This game was a push!")
        
"""
Handle everything that happens when a user commands $score, will post the current score of an
ongoing game or post a past game

"""
async def handle_score_command(r, message):
    if("vs" in message.content):
        if(message.content.startswith('$score')):
           teams = message.content.split("$score")[1]
        elif(message.content.startswith('$Score')):
            teams = message.content.split("$Score")[1]

        home_team = teams.split("vs")[0].strip()
        away_team = teams.split("vs")[1].strip()
        
        # Parse the season number from string
        parse_season_dict = parse_season(away_team)
        away_team = parse_season_dict[1]
        season = parse_season_dict[2]
        postseason = parse_season_dict[3]
            
        lookingForThread = await message.channel.send("Looking for the game thread...")
        print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + home_team + " vs " + away_team)
        
        home_team = changeUserInputTeams(home_team)
        away_team = changeUserInputTeams(away_team)
        
        submission = searchForGameThread(r, home_team, away_team, season, "$score", postseason)
        if(submission == "NONE"):
            await message.channel.send("No game thread found.")
        else:
            print("GAME THREAD FOUND")
            
            url = saveGithubData(submission.selftext, season)
            home_team = parse_home_team(submission.selftext)
            away_team = parse_away_team(submission.selftext)
                        
            # Hardcode to fix inconsistencies in stat sheets
            home_team = handleNamingInconsistincies(home_team)
            away_team = handleNamingInconsistincies(away_team)
              
            # Get the vegas odds
            vegas_odds_dict = getVegasOdds(home_team, away_team)
            if "The following error occured:" not in vegas_odds_dict:
                home_vegas_odds = vegas_odds_dict[1]
                away_vegas_odds = vegas_odds_dict[2]
                # Get the score
                home_score = parse_home_score(submission.selftext)
                away_score = parse_away_score(submission.selftext)
                    
                if("Game complete" in submission.selftext):
                    if(season == "S6"):
                        if(int(home_score) > int(away_score) or int(home_score) == int(away_score)):
                            await make_game_final_score_post(message, submission, home_team, away_team, home_vegas_odds, home_score, away_score)
                        elif(int(home_score) < int(away_score)):
                            await make_game_final_score_post(message, submission, away_team, home_team, away_vegas_odds, away_score, home_score)  
                    else:
                        post = "blank"
                        if(int(home_score) > int(away_score)):
                            post = "**FINAL | " + home_team + " defeated " + away_team + " " + home_score + "-" + away_score + "**\n"
                        else:
                            post = "**FINAL | " + away_team + " defeated " + home_team + " " + away_score + "-" + home_score + "**\n"
                        await message.channel.send(post)
                else:
                    if(season == "S6"):
                        await get_ongoing_game_information(message, submission, home_vegas_odds, away_vegas_odds, home_team, away_team, home_score, away_score)
                    
                    else:
                        post = "blank"
                        if(int(home_score) > int(away_score)):
                            post = "**FINAL | " + home_team + " defeated " + away_team + " " + home_score + "-" + away_score + "**\n"
                        else:
                            post = "**FINAL | " + away_team + " defeated " + home_team + " " + away_score + "-" + home_score + "**\n"
                        await message.channel.send(post) 
            else:
                await message.channel.send("**Vegas odds retrieval error**\n\n" + vegas_odds_dict)
            
                 
        await lookingForThread.delete()
    else: 
        await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")
        
"""
Handle everything that happens when a user commands $plot, will post the current plot of an
ongoing game or post a past game

"""    
async def handle_plot_command(r, message):
    if("vs" in message.content):
        if(message.content.startswith('$plot')):
           teams = message.content.split("$plot")[1]
        elif(message.content.startswith('$Plot')):
            teams = message.content.split("$Plot")[1]

        home_team = teams.split("vs")[0].strip()
        away_team = teams.split("vs")[1].strip()
        
        # Parse the season number from string
        parse_season_dict = parse_season(away_team)
        away_team = parse_season_dict[1]
        season = parse_season_dict[2]
        postseason = parse_season_dict[3]
        
        lookingForThread = await message.channel.send("Looking for the game thread...")
        print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + home_team + " vs " + away_team)
        
        home_team = changeUserInputTeams(home_team)
        away_team = changeUserInputTeams(away_team)
        
        # Look for game thread
        submission = searchForGameThread(r, home_team, away_team, season, "$plot", postseason)
        if(submission == "NONE"):
            await message.channel.send("No game thread found.")
        else:
            print("GAME THREAD FOUND")
            
            # Parse data from url
            url = saveGithubData(submission.selftext, season)
            home_team = parse_home_team(submission.selftext)
            away_team = parse_away_team(submission.selftext)
                        
            # Hardcode to fix inconsistencies in stat sheets
            home_team = handleNamingInconsistincies(home_team)
            away_team = handleNamingInconsistincies(away_team)
             
            #Get team colors for plots
            colorDict = getTeamColors(home_team, away_team)
            if "The following error occured:" not in colorDict:
                home_color = colorDict[1]
                away_color = colorDict[2]
                vegas_odds_dict = getVegasOdds(home_team, away_team)
                # Get the vegas odds
                if "The following error occured:" not in vegas_odds_dict:
                    home_vegas_odds = vegas_odds_dict[1]
                    away_vegas_odds = vegas_odds_dict[2]
                    #Work with new gist
                    if(season == "S6" or season == "S5" or season == "S4"):
                        if("Game complete" in submission.selftext):
                            #If there is a GitHub URL as plays have been called
                            if(url != "NO PLAYS"):
                                # Iterate through the data and plot the graphs
                                iterate_through_game_gist(home_team, away_team, home_color, away_color)
                                
                                # Send score plot
                                with open('output.png', 'rb') as fp:
                                    await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                                    
                                # Send the win probability plot
                                with open('outputwin_probability.png', 'rb') as fp:
                                    await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                            else:
                                await message.channel.send("No plays for the game found.")
                        else:
                            #If there is a GitHub URL as plays have been called
                            if(url != "NO PLAYS"):
                                # Iterate through the data and plot the graphs
                                iterate_through_game_gist(home_team, away_team, home_color, away_color)
                                
                                # Send score plot
                                with open('output.png', 'rb') as fp:
                                    await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                                    
                                # Send the win probability plot
                                with open('outputwin_probability.png', 'rb') as fp:
                                    await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                            else:
                                await message.channel.send("No plays for the game found.")
                    else:
                        # Get game thread submission day
                        submission_time = datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
                        year = int(submission_time.split("-")[0])
                        month = int(submission_time.split("-")[1])
                        day = int(submission_time.split("-")[2].split(" ")[0])
                        if(year > 2018 or (year == 2018 and month == 8 and day > 25) or (year == 2018 and month > 8)):
                            old_thread = await message.channel.send("Iterating through old thread to generate plots...")
                            await message.channel.send("**PLEASE NOTE DUE TO HOW THIS DATA WAS GATHERED THAT THIS PLOT IS NOT THE CURRENT MODEL WIN PROBABILITY**")
                            threadCrawler(home_team, away_team, home_vegas_odds, away_vegas_odds, home_color, away_color, season, submission)
                            # Send score plot
                            with open('output.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                                    
                            # Send the win probability plot
                            with open('outputwin_probability.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                            await old_thread.delete()
                        else:
                            await message.channel.send("This game is too old to plot the data. I can only plot Season I, Week 11 games onward")
                else:
                    await message.channel.send("**Vegas odds retrieval error**\n\n" + vegas_odds_dict)
            else:
                await message.channel.send("**Color retrieval error**\n\n" + colorOddsDict)

            
        await lookingForThread.delete()
    else: 
        await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")

"""
Handle when the user requests the conference standings

"""
async def handle_standings_command(r, message):
    if(message.content.startswith('$standings')):
        conference = message.content.split("$standings")[1].strip()
    elif(message.content.startswith('$Standings')):
        conference = message.content.split("$Standings")[1].strip()
    elif(message.content.startswith('$standing')):
        conference = message.content.split("$standing")[1].strip()
    elif(message.content.startswith('$Standing')):
        conference = message.content.split("$Standing")[1].strip()
    post = getStandingsData(conference)
    await message.channel.send(post)
    
"""
Handle when the user requests a ranking

"""    
async def handle_rankings_command(r, message):
    if(message.content.startswith('$rankings')):
        request = message.content.split("$rankings")[1].strip()
    elif(message.content.startswith('$Rankings')):
        request = message.content.split("$Rankings")[1].strip()
    if(request == "" or request == " "):
        await message.channel.send("The $rankings command currently supports the following ranks commands:\n" +
                                   "- FBS Coaches Poll\n- FCS Coaches Poll\n- FBS Elo\n- FCS Elo\n- MOV (FBS Only)\n- Scoring Offense (FBS Only)\n- Scoring Defense (FBS Only)\n" + 
                                   "- SOSMOV (FBS Only)\n- EQW (FBS Only)\n- Composite (FBS Only)\n- Adjusted Strength Rating (FBS Only)\n- Colley Matrix (FBS Only)\n" + 
                                   "- Adjusted Speed (FBS Only)\n" + "- Raw Speed (FBS Only)\n" + "**If you want a ranking added, please contact Dick**")
    else:
        post = getRankingsData(r, request)
        await message.channel.send(post)

"""
Handle when the user requests a team's opponent

"""   
async def handle_opponent_command(r, message):
    if(message.content.startswith('$opponent')):
        team = message.content.split("$opponent")[1].strip()
    elif(message.content.startswith('$Opponent')):
        team = message.content.split("$Opponent")[1].strip()

    lookingForThread = await message.channel.send("Looking for the most recent game thread with the following team: " + team)
    print("LOOKING FOR THREAD WITH THE FOLLOWING TEAM: " + team)
    
    team = changeUserInputTeams(team)
    
    opponent = searchForTeamGameThread(r, team) 
    # opponent[1] is team, opponent[2] is the opponent
    if(opponent[1] == "NONE"):
        await message.channel.send("No game thread found.")
    else:
        await message.channel.send(opponent[1] + " is playing " + opponent[2])
    await lookingForThread.delete()

"""
Login to Discord and run the bot

"""
def login_discord(r):
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    token = config_data['discord_token']

    client = discord.Client()

    @client.event
    async def on_message(message):
        global postEdited, changeIndex
        
        if(message.content.startswith('$score') or message.content.startswith('$Score')):
           await handle_score_command(r, message)
        
        elif(message.content.startswith('$plot') or message.content.startswith('$Plot')):
            await handle_plot_command(r, message)
            
        elif(message.content.startswith('$Standings') or message.content.startswith('$standings') or 
             message.content.startswith('$Standing') or message.content.startswith('$standing')):
            await handle_standings_command(r, message)
            
        elif(message.content.startswith('$Rankings') or message.content.startswith('$rankings')):
            await handle_rankings_command(r, message)

        elif(message.content.startswith('$Opponent') or message.content.startswith('$opponent')):
            await handle_opponent_command(r, message)
                
    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token) 