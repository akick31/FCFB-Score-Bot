import praw
import discord
import json
import datetime
from discord.ext import commands
from name_fix import *
from vegas_odds import *
from color import *
from game_data import *
from game_thread_data import *
from gist_data import *
from thread_crawler import *
from win_probability import *
from sheets_functions import *

with open('season_information.json', 'r') as config_file:
    season_info_data = json.load(config_file)

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
    season = season_info_data['current_season']
    if season_info_data['seasons'] in away_team.lower():
        team_split = away_team.split(" ")
        i = 0
        for split in team_split:
            split = split.lower()
            if season_info_data['seasons'] in split:
                season = team_split[i]
            if "postseason" in split:
                postseason = 1
            i = i + 1
        away_team = away_team.split(season)[0] 
        away_team = away_team.strip()
    return {1: away_team, 2: season, 3: postseason}


"""
Make posts for ongoing games on Reddit

"""


async def make_ongoing_game_post(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, vegasOdds, team, opponentTeam, score, opponentScore, cur_win_probability, waiting_on):
    odds = round(vegasOdds * 2) / 2
    if odds == 0:
        odds = "Push"
    elif odds > 0:
        odds = "+" + str(odds)
    post = "**" + cur_clock + " | " + opponentTeam + " " + opponentScore + " " + team + " " + score + " (" + str(odds) + ")** \n"
    yard_post = cur_down + " | :football: " + cur_possession + " | " + cur_yard_line + "\n"
    win_post = "Each team has a 50% chance to win\n"
    if int(cur_win_probability) >= 50:
        win_post = team + " has a " + str(int(cur_win_probability)) + "% chance to win\n"
    elif int(cur_win_probability) < 50:
        win_post = opponentTeam + " has a " + str(100-int(cur_win_probability)) + "% chance to win\n"
    waiting_on_post = "Waiting on " + waiting_on + " for a number\n"
    await message.channel.send(post + yard_post + win_post + waiting_on_post + submission.url + "\n")


"""
Get information to make a post for ongoing games on Reddit

"""


async def get_ongoing_game_information(message, submission, home_vegas_odds, away_vegas_odds, home_team, away_team, home_score, away_score):
    # Get win probability
    cur_possession = parse_possession(submission.selftext)
    offense_win_probability = get_in_game_win_probability(home_team, away_team)
    print(offense_win_probability)
    if cur_possession == home_team:
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
    if cur_quarter == "OT":
        cur_clock = "OT"
    else:
        cur_clock = str(cur_time) + " " + str(cur_quarter)

    # If home team is winning or the score is tied
    if int(home_score) > int(away_score) or int(home_score) == int(away_score):
        await make_ongoing_game_post(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, home_vegas_odds, home_team, away_team, home_score, away_score, home_win_probability, waiting_on)
    # If the home team is losing
    elif int(home_score) < int(away_score):
        await make_ongoing_game_post(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, away_vegas_odds, away_team, home_team, away_score, home_score, away_win_probability, waiting_on)


"""
Make posts for games that went final on Reddit

"""


async def make_game_final_score_post(message, team, opponent_team, vegas_odds, score, opponent_score):
    odds = round(vegas_odds * 2) / 2
    number_odds = odds
    if odds == 0:
        odds = "Push"
    elif odds > 0:
        odds = "+" + str(odds)
    post = "**FINAL | " + team + " defeated " + opponent_team + " " + score + "-" + opponent_score + "**\n"
    if int(number_odds) > 0:
        await message.channel.send(post + "UPSET! " + team + " was underdogs at " + str(odds) + " and won!")
    if int(number_odds) < 0 and (int(opponent_score) - int(score)) > number_odds:
        await message.channel.send(post + opponent_team + " beat the spread listed at " + str(odds))
    elif int(number_odds) < 0 and (int(opponent_score) - int(score)) < number_odds:
        print(number_odds)
        await message.channel.send(post + team + " covered the spread listed at " + str(odds))
    if int(number_odds) == 0 or (int(opponent_score) - int(score)) == number_odds:
        await message.channel.send(post + "This game was a push!")


"""
Handle everything that happens when a user commands $score, will post the current score of an
ongoing game or post a past game

"""


async def handle_score_command(r, message):
    message_content = message.content.lower()
    if "vs" in message.message_content:
        teams = message_content.split("$score")[1]

        home_team = teams.split("vs")[0].strip()
        away_team = teams.split("vs")[1].strip()
        
        # Parse the season number from string
        parse_season_dict = parse_season(away_team)
        away_team = parse_season_dict[1]
        season = parse_season_dict[2].lower()
        postseason = parse_season_dict[3]
            
        looking_for_thread = await message.channel.send("Looking for the game thread...")
        print("LOOKING FOR THREAD WITH THE FOLLOWING MATCH UP: " + home_team + " vs " + away_team)

        # Fix the inputted user team for naming inconsistencies
        home_team = fix_user_input_teams(home_team)
        away_team = fix_user_input_teams(away_team)
        
        submission = search_for_game_thread(r, home_team, away_team, season, "$score", postseason)
        if submission == "NONE":
            await message.channel.send("No game thread found.")
        else:
            print("GAME THREAD FOUND")
            
            url = save_github_data(submission.selftext, season)
            home_team = parse_home_team(submission.selftext)
            away_team = parse_away_team(submission.selftext)
                        
            # Hardcode to fix inconsistencies in stat sheets
            home_team = handle_naming_inconsistencies(home_team)
            away_team = handle_naming_inconsistencies(away_team)
              
            # Get the vegas odds
            vegas_odds_dict = get_vegas_odds(home_team, away_team)
            if "The following error occured:" not in vegas_odds_dict:
                home_vegas_odds = vegas_odds_dict[1]
                away_vegas_odds = vegas_odds_dict[2]

                # Get the score
                home_score = parse_home_score(submission.selftext)
                away_score = parse_away_score(submission.selftext)
                    
                if "Game complete" in submission.selftext:
                    if season == season_info_data['current_season']:
                        if int(home_score) > int(away_score) or int(home_score) == int(away_score):
                            await make_game_final_score_post(message, home_team, away_team, home_vegas_odds, home_score, away_score)
                        elif int(home_score) < int(away_score):
                            await make_game_final_score_post(message, away_team, home_team, away_vegas_odds, away_score, home_score)
                    else:
                        post = "blank"
                        if int(home_score) > int(away_score):
                            post = "**FINAL | " + home_team + " defeated " + away_team + " " + home_score + "-" + away_score + "**\n"
                        else:
                            post = "**FINAL | " + away_team + " defeated " + home_team + " " + away_score + "-" + home_score + "**\n"
                        await message.channel.send(post)
                else:
                    if season == season_info_data['current_season']:
                        await get_ongoing_game_information(message, submission, home_vegas_odds, away_vegas_odds, home_team, away_team, home_score, away_score)
                    
                    else:
                        post = "blank"
                        if int(home_score) > int(away_score):
                            post = "**FINAL | " + home_team + " defeated " + away_team + " " + home_score + "-" + away_score + "**\n"
                        else:
                            post = "**FINAL | " + away_team + " defeated " + home_team + " " + away_score + "-" + home_score + "**\n"
                        await message.channel.send(post) 
            else:
                await message.channel.send("**Vegas odds retrieval error**\n\n" + vegas_odds_dict)

        await looking_for_thread.delete()
    else: 
        await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")


"""
Handle everything that happens when a user commands $plot, will post the current plot of an
ongoing game or post a past game

"""


async def handle_plot_command(r, message):
    message_content = message.content.lower()
    if "vs" in message.content:
        teams = message_content.split("$plot")[1]

        home_team = teams.split("vs")[0].strip()
        away_team = teams.split("vs")[1].strip()
        
        # Parse the season number from string
        parse_season_dict = parse_season(away_team)
        away_team = parse_season_dict[1]
        season = parse_season_dict[2].lower()
        postseason = parse_season_dict[3]
        
        looking_for_thread = await message.channel.send("Looking for the game thread...")
        print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + home_team + " vs " + away_team)
        
        home_team = fix_user_input_teams(home_team)
        away_team = fix_user_input_teams(away_team)
        
        # Look for game thread
        submission = search_for_game_thread(r, home_team, away_team, season, "$plot", postseason)
        if submission == "NONE" :
            await message.channel.send("No game thread found.")
        else:
            print("GAME THREAD FOUND")
            
            # Parse data from url
            url = save_github_data(submission.selftext, season)
            home_team = parse_home_team(submission.selftext)
            away_team = parse_away_team(submission.selftext)
                        
            # Hardcode to fix inconsistencies in stat sheets
            home_team = handle_naming_inconsistencies(home_team)
            away_team = handle_naming_inconsistencies(away_team)
             
            # Get team colors for plots
            color_dict = getTeamColors(home_team, away_team)
            if "The following error occurred:" not in color_dict:
                home_color = color_dict[1]
                away_color = color_dict[2]
                vegas_odds_dict = get_vegas_odds(home_team, away_team)
                # Get the vegas odds
                if "The following error occurred:" not in vegas_odds_dict:
                    home_vegas_odds = vegas_odds_dict[1]
                    away_vegas_odds = vegas_odds_dict[2]

                    # Work with new gist
                    if season == "S6" or season == "S5" or season == "S4":
                        # If there is a GitHub URL as plays have been called
                        if url != "NO PLAYS":
                            # Iterate through the data and plot the graphs
                            iterate_through_game_gist(home_team, away_team, home_color, away_color)

                            # Send score plot
                            with open('output.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_filename.png'))

                            # Send the win probability plot
                            with open('output_win_probability.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                        else:
                            await message.channel.send("No plays for the game found.")
                    else:
                        # Get game thread submission day
                        submission_time = datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
                        year = int(submission_time.split("-")[0])
                        month = int(submission_time.split("-")[1])
                        day = int(submission_time.split("-")[2].split(" ")[0])
                        if year > 2018 or (year == 2018 and month == 8 and day > 25) or (year == 2018 and month > 8):
                            old_thread = await message.channel.send("Iterating through old thread to generate plots...")
                            await message.channel.send("**PLEASE NOTE DUE TO HOW THIS DATA WAS GATHERED THAT THIS PLOT " +
                                                        "IS NOT THE CURRENT MODEL WIN PROBABILITY**")
                            thread_crawler(home_team, away_team, home_vegas_odds, away_vegas_odds, home_color, away_color, season, submission)
                            # Send score plot
                            with open('output.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                                    
                            # Send the win probability plot
                            with open('output_win_probability.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                            await old_thread.delete()
                        else:
                            await message.channel.send("This game is too old to plot the data. I can only plot Season I, " +
                                                       "Week 11 games onward")
                else:
                    await message.channel.send("**Vegas odds retrieval error**\n\n" + vegas_odds_dict)
            else:
                await message.channel.send("**Color retrieval error**\n\n" + color_dict)
            
        await looking_for_thread.delete()
    else: 
        await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")


"""
Handle when the user requests the conference standings

"""


async def handle_standings_command(r, message):
    message_content = message.content.lower()
    conference = message_content.split("$standing")[1].strip()

    post = get_standings_data(conference)
    await message.channel.send(post)


"""
Handle when the user requests a ranking

"""


async def handle_rankings_command(r, message):
    message_content = message.content.lower()
    request = message_content.split("$rankings")[1].strip()

    if request == "" or request == " ":
        await message.channel.send("The $rankings command currently supports the following ranks commands:\n" +
                                   "- FBS Coaches Poll\n- FCS Coaches Poll\n- FBS Elo\n- FCS Elo\n- MOV (FBS Only)\n" +
                                   "- Scoring Offense (FBS Only)\n- Scoring Defense (FBS Only)\n" +
                                   "- SOSMOV (FBS Only)\n- EQW (FBS Only)\n- Composite (FBS Only)\n" +
                                   "- Adjusted Strength Rating (FBS Only)\n- Colley Matrix (FBS Only)\n" +
                                   "- Adjusted Speed (FBS Only)\n" + "- Raw Speed (FBS Only)\n" +
                                   "**If you want a ranking added, please contact Dick**")
    else:
        post = getRankingsData(r, request)
        await message.channel.send(post)


"""
Handle when the user requests a team's opponent

"""


async def handle_opponent_command(r, message):
    message_content = message.content.lower()
    team = message_content.split("$opponent")[1].strip()

    looking_for_thread = await message.channel.send("Looking for the most recent game thread with the following team: "
                                                    + team)
    print("LOOKING FOR THREAD WITH THE FOLLOWING TEAM: " + team)
    
    team = fix_user_input_teams(team)
    
    opponent = search_for_team_game_thread(r, team)
    # opponent[1] is team, opponent[2] is the opponent
    if opponent[1] == "NONE":
        await message.channel.send("No game thread found.")
    else:
        await message.channel.send(opponent[1] + " is playing " + opponent[2])
    await looking_for_thread.delete()


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
        message_content = message.content.lower()
        
        if message_content.startswith('$score'):
            await handle_score_command(r, message)
        
        elif message_content.startswith('$plot'):
            await handle_plot_command(r, message)
            
        elif message_content.startswith('$standing'):
            await handle_standings_command(r, message)
            
        elif message_content.startswith('$rankings'):
            await handle_rankings_command(r, message)

        elif message_content.startswith('$opponent'):
            await handle_opponent_command(r, message)
                
    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token)