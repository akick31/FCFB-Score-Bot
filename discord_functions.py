import praw
import discord
import json
import datetime
from discord.ext import commands
from name_fix import *
from vegas_odds import *
from color import *
from parse_game_data import *
from game_thread_information import *
from gist_data import *
from thread_crawler import *
from win_probability import *
from sheets_functions import *
from reddit_functions import *
from database_functions import *

with open('/home/ubuntu/FCFB/FCFB-Score-Bot/season_information.json', 'r') as config_file:
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
    for season in season_info_data['seasons'].keys():
        if season in away_team.lower():
            team_split = away_team.split(" ")
            for split in team_split:
                split = split.lower()
                if season == split:
                    season = split
                    if "postseason" in team_split:
                        postseason = 1
                    away_team = away_team.split(season)[0]
                    away_team = away_team.strip()
                    return {1: away_team, 2: season, 3: postseason}
            away_team = away_team.split(season)[0]
            away_team = away_team.strip()
    return {1: away_team, 2: season, 3: postseason}


"""
Handle everything that happens when a user commands $score, will post the current score of an
ongoing game or post a past game

"""


async def handle_score_command(r, message, database):
    message_content = message.content.lower()
    print(message_content)

    if "vs" in message_content:
        teams = message_content.split("$score")[1]

        home_team = teams.split("vs")[0].strip()
        away_team = teams.split("vs")[1].strip()

        # Parse the season number from string
        parse_season_dict = parse_season(away_team)
        away_team = parse_season_dict[1]
        season = parse_season_dict[2].lower()
        postseason = parse_season_dict[3]
        
        # Fix the inputted user team for naming inconsistencies
        home_team = fix_user_input_teams(home_team)
        away_team = fix_user_input_teams(away_team)
    else:
        home_team = message_content.split("$score")[1].strip()
        
        # Fix the inputted user team for naming inconsistencies
        home_team = fix_user_input_teams(home_team)

        opponent = search_for_team_game_thread(r, home_team)
        # opponent[1] is team, opponent[2] is the opponent
        if opponent[1] == "NONE":
            await message.channel.send("Could not find opponent for " + home_team + ". No game thread found.")
            print("Could not find opponent for " + home_team + "\n")
            return
        else:
            away_team = opponent[2]
            
            # Fix the inputted user team for naming inconsistencies
            away_team = fix_user_input_teams(away_team)
            
            season = season_info_data['current_season']
            postseason = 0
            
    looking_for_thread = await message.channel.send("Looking for the game thread...")
    print("LOOKING FOR THREAD WITH THE FOLLOWING MATCH UP: " + home_team + " vs " + away_team)
    
    submission = search_for_game_thread(r, home_team, away_team, season, "$score", postseason)
    if submission == "NONE":
        await message.channel.send("No game thread found for " + home_team + " vs " + away_team)
        print("No game thread found for " + home_team + " vs " + away_team + "\n")

    else:
        print("GAME THREAD FOUND")

        url = save_github_data(submission.selftext, season)
        home_team = parse_home_team(submission.selftext)
        away_team = parse_away_team(submission.selftext)

        # Hardcode to fix inconsistencies in stat sheets
        home_team = handle_naming_inconsistencies(home_team)
        away_team = handle_naming_inconsistencies(away_team)

        # Get the vegas odds
        vegas_odds_dict = get_vegas_odds(home_team, away_team, database)
        if vegas_odds_dict is not None:
            home_vegas_odds = vegas_odds_dict[1]
            away_vegas_odds = vegas_odds_dict[2]

            # Get the score
            home_score = parse_home_score(submission.selftext)
            away_score = parse_away_score(submission.selftext)

            home_record = parse_home_record(submission.title)
            away_record = parse_away_record(submission.title)

            if "Game complete" in submission.selftext:
                if season == season_info_data['current_season']:
                    await craft_game_final_score_comment(message, submission, home_team, away_team, home_vegas_odds,
                                                         home_score, away_score, home_record, away_record)
                else:
                    await craft_game_final_score_comment(message, submission, home_team, away_team, "NONE",
                                                         home_score, away_score, home_record, away_record)
            else:
                if season == season_info_data['current_season']:
                    await get_ongoing_game_information(database, message, submission, home_vegas_odds, away_vegas_odds,
                                                       home_team, away_team, home_score, away_score)

                else:
                    await craft_game_final_score_comment(message, submission, home_team, away_team, "NONE",
                                                         home_score, away_score, home_record, away_record)
        else:
            await message.channel.send("The following error occurred: vegas odds retrieval error")

    await looking_for_thread.delete()


"""
Handle everything that happens when a user commands $plot, will post the current plot of an
ongoing game or post a past game

"""


async def handle_plot_command(r, message, database):
    message_content = message.content.lower()

    if "vs" in message_content:
        teams = message_content.split("$plot")[1]

        home_team = teams.split("vs")[0].strip()
        away_team = teams.split("vs")[1].strip()

        # Parse the season number from string
        parse_season_dict = parse_season(away_team)
        away_team = parse_season_dict[1]
        season = parse_season_dict[2].lower()
        postseason = parse_season_dict[3]
    else:
        home_team = message_content.split("$plot")[1].strip()
        opponent = search_for_team_game_thread(r, home_team)
        # opponent[1] is team, opponent[2] is the opponent
        if opponent[1] == "NONE":
            await message.channel.send("Could not find opponent for " + home_team + ". No game thread found.")
            print("Could not find opponent for " + home_team + "\n")
            return
        else:
            away_team = opponent[2]
            season = season_info_data['current_season']
            postseason = 0

    looking_for_thread = await message.channel.send("Looking for the game thread...")
    print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + home_team + " vs " + away_team)

    home_team = fix_user_input_teams(home_team)
    away_team = fix_user_input_teams(away_team)

    # Look for game thread
    submission = search_for_game_thread(r, home_team, away_team, season, "$plot", postseason)
    if submission == "NONE":
        await message.channel.send("No game thread found for " + home_team + " vs " + away_team)
        print("No game thread found for " + home_team + " vs " + away_team + "\n")
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
        color_dict = get_team_colors(home_team, away_team)
        if "The following error occurred:" not in color_dict:
            home_color = color_dict[1]
            away_color = color_dict[2]
            vegas_odds_dict = get_vegas_odds(home_team, away_team, database)
            # Get the vegas odds
            if vegas_odds_dict is not None:
                home_vegas_odds = vegas_odds_dict[1]
                away_vegas_odds = vegas_odds_dict[2]
                season_num = int(season.split("s")[1])

                # Work with new gist
                if season_num >= 4:
                    # If there is a GitHub URL as plays have been called
                    if url != "NO PLAYS":
                        # Iterate through the data and plot the graphs
                        iterate_through_game_gist(database, home_team, away_team, home_color, away_color)

                        # Send score plot
                        with open('/home/ubuntu/FCFB/FCFB-Score-Bot/output.png', 'rb') as fp:
                            await message.channel.send(file=discord.File(fp, '/home/ubuntu/FCFB/FCFB-Score-Bot/new_filename.png'))

                        # Send the win probability plot
                        with open('/home/ubuntu/FCFB/FCFB-Score-Bot/output_win_probability.png', 'rb') as fp:
                            await message.channel.send(file=discord.File(fp, '/home/ubuntu/FCFB/FCFB-Score-Bot/new_win_probability.png'))
                        print("Plot posted for " + home_team + " vs " + away_team + "\n\n")
                    else:
                        await message.channel.send("Could not generate plot for " + home_team + " vs " + away_team)
                        print("Could not post plot for " + home_team + " vs " + away_team + "\n")
                else:
                    # Get game thread submission day
                    submission_time = datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
                    year = int(submission_time.split("-")[0])
                    month = int(submission_time.split("-")[1])
                    day = int(submission_time.split("-")[2].split(" ")[0])
                    if year > 2018 or (year == 2018 and month == 8 and day > 25) or (year == 2018 and month > 8):
                        old_thread = await message.channel.send("Iterating through old thread to generate plots...")
                        await message.channel.send("Please note due to how this data was gathered that this plot does" +
                                                   "not use the current win probability model, so it is slightly inaccurate.")
                        thread_crawler(home_team, away_team, home_vegas_odds, away_vegas_odds, home_color, away_color, season, submission)
                        # Send score plot
                        with open('/home/ubuntu/FCFB/FCFB-Score-Bot/output.png', 'rb') as fp:
                            await message.channel.send(file=discord.File(fp, '/home/ubuntu/FCFB/FCFB-Score-Bot/new_filename.png'))

                        # Send the win probability plot
                        with open('/home/ubuntu/FCFB/FCFB-Score-Bot/output_win_probability.png', 'rb') as fp:
                            await message.channel.send(file=discord.File(fp, '/home/ubuntu/FCFB/FCFB-Score-Bot/new_win_probability.png'))
                        await old_thread.delete()
                        print("Old plot posted for " + home_team + " vs " + away_team + "\n\n")
                    else:
                        await message.channel.send("This game is too old to plot the data. I can only plot Season I, " +
                                                   "Week 11 games onward")
                        print("Could not post old plot for " + home_team + " vs " + away_team + "\n\n")
            else:
                await message.channel.send("**Vegas odds retrieval error, please check logs for more information**")
        else:
            await message.channel.send("**Color retrieval error**\n\n" + color_dict)

    await looking_for_thread.delete()




"""
Handle when the user requests the conference standings

"""


async def handle_standings_command(r, message, database):
    print("Getting rankings information")
    message_content = message.content.lower()
    if "$standing " in message_content:
        conference = message_content.split("$standing")[1].strip()
    else:
        conference = message_content.split("$standings")[1].strip()

    post = get_standings_data(conference)
    await message.channel.send(post)
    print("Posted result of the standings command!")


"""
Handle when the user requests a ranking

"""


async def handle_rankings_command(r, message, database):
    print("Getting rankings information")
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
        post = get_rankings_data(r, request, database)
        await message.channel.send(post)
        print("Posted result of the rankings command!")
        
"""
Handle when the user requests a team's opponent

"""


async def handle_opponent_command(r, message, database):
    message_content = message.content.lower()
    team = message_content.split("$opponent")[1].strip()

    looking_for_thread = await message.channel.send("Looking for the most recent game thread with the following team: "
                                                    + team)
    print("LOOKING FOR THREAD WITH THE FOLLOWING TEAM: " + team)
    
    team = fix_user_input_teams(team)
    
    opponent = search_for_team_game_thread(r, team)
    # opponent[1] is team, opponent[2] is the opponent
    if opponent[1] == "NONE":
        await message.channel.send("Could not find opponent for " + team + ". No game thread found.")
        print("Could not find opponent for " + team + "\n")
    else:
        await message.channel.send(opponent[1] + " is playing " + opponent[2])
        print("Opponent posted for " + team + "\n\n")
    await looking_for_thread.delete()


"""
Handle when the user requests to start games

"""


async def handle_start_games_command(r, message):
    print("STARTING GAMES")
    await message.channel.send("Starting games for this week")
    message_content = message.content.lower()
    game_start_commands = parse_game_start_commands()
    for command in game_start_commands:
        print(command)
        try:
            r.redditor("NFCAAOfficialRefBot").message("newgame", command)
        except Exception as e:
            print(e)
            print("Rate limit, waiting 400 seconds...")
            await message.channel.send("Rate limit, waiting 400 seconds...")
            time.sleep(400)
            await message.channel.send("Continuing...")
            r.redditor("NFCAAOfficialRefBot").message("newgame", command)
    print("DONE STARTING GAMES")
    await message.channel.send("Done starting games for this week")


"""
Handle resetting the week flag in config.json

"""


async def handle_reset_week_command(config_data, message):
    if config_data['week_run'] == "NO":
        print("Reset week_run flag in config.json to YES")
        config_data['week_run'] = "YES"
        await message.channel.send("Manually marked games for this week as done, you can no longer use $start_games to start games until this command is run again to clear the flag")
    else:
        print("Reset week_run flag in config.json to NO")
        config_data['week_run'] = "NO"
        await message.channel.send("Reset the flag to start games, you may now use $start_games to start the games for the week")


"""
Handle resetting the week flag in config.json

"""


async def handle_team_command(config_data, message, database):
    message_content = message.content.lower()
    team = message_content.split("$team")[1].strip()
        
    # Fix the inputted user team for naming inconsistencies
    fixed_team = fix_user_input_teams(team)

    information_list = get_team_information(database, fixed_team)
    embed = discord.Embed(
        title="Iowa State", description="All-Time Information", color=0x00b300)
    embed.add_field(name="Current Coach", value=information_list[0], inline=True)
    embed.add_field(name="Number of Coaches", value=information_list[1], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Winningest Coach", value=information_list[2], inline=True)
    embed.add_field(name="Longest Serving Coach", value=information_list[3], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="All-Time Record", value=information_list[4], inline=True)
    embed.add_field(name="All-Time Winning Percentage", value=information_list[5], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Conference Record", value=information_list[6], inline=True)
    embed.add_field(name="Conference Winning Percentage", value=information_list[7], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Division Record", value=information_list[6], inline=True)
    embed.add_field(name="Division Winning Percentage", value=information_list[7], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Out of Conference Record", value=information_list[6], inline=True)
    embed.add_field(name="Out of Conference Winning Percentage", value=information_list[7], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Record vs Ranked", value=information_list[6], inline=True)
    embed.add_field(name="Winning Percentage vs Ranked", value=information_list[7], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Record as Ranked", value=information_list[6], inline=True)
    embed.add_field(name="Winning Percentage as Ranked", value=information_list[7], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Highest Rank", value=information_list[6], inline=True)
    embed.add_field(name="Weeks Ranks", value=information_list[7], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Bowl Record", value=information_list[6], inline=True)
    embed.add_field(name="Bowl Winning Percentage", value=information_list[7], inline=True)
    embed.addField('\u200b', '\u200b')
    embed.add_field(name="Conference Championship Record", value=information_list[6], inline=True)
    embed.add_field(name="Conference Championship Winning Percentage", value=information_list[7], inline=True)
    embed.add_field(name="Playoff Appearances", value=information_list[6], inline=True)
    embed.add_field(name="Playoff Record", value=information_list[6], inline=True)
    embed.add_field(name="Playoff Winning Percentage", value=information_list[7], inline=True)
    embed.add_field(name="National Championships", value=information_list[6], inline=True)
  
    await message.channel.send(embed=embed)
    return


"""
Login to Discord and run the bot

"""


def login_discord(r):
    with open('/home/ubuntu/FCFB/FCFB-Score-Bot/config.json', 'r') as config_file:
        config_data = json.load(config_file)

    token = config_data['discord_token']

    client = discord.Client()

    @client.event
    async def on_message(message): 
        message_content = message.content.lower()
        
        if message_content.startswith('$score'):
            database = connect_to_database()
            if database == None:
                await message.channel.send("Cannot connect to database, please try again later.")
            else:
                await handle_score_command(r, message, database)
                close_database(database)
        
        elif message_content.startswith('$plot'):
            database = connect_to_database()
            if database == None:
                await message.channel.send("Cannot connect to database, please try again later.")
            else:
                await handle_plot_command(r, message, database)
                close_database(database)
            
        elif message_content.startswith('$standing'):
            database = connect_to_database()
            if database == None:
                await message.channel.send("Cannot connect to database, please try again later.")
            else:
                await handle_standings_command(r, message, database)
                close_database(database)
            
        elif message_content.startswith('$rankings'):
            database = connect_to_database()
            if database == None:
                await message.channel.send("Cannot connect to database, please try again later.")
            else:
                await handle_rankings_command(r, message, database)
                close_database(database)

        elif message_content.startswith('$opponent'):
            database = connect_to_database()
            if database == None:
                await message.channel.send("Cannot connect to database, please try again later.")
            else:
                await handle_opponent_command(r, message, database)
                close_database(database)

        elif message_content.startswith('$team'):
            database = connect_to_database()
            if database == None:
                await message.channel.send("Cannot connect to database, please try again later.")
            else:
                await handle_team_command(r, message, database)
                close_database(database)

        nfcaa_office = discord.utils.find(lambda r: r.name == 'NFCAA Office', message.guild.roles)
        fbs_commissioner = discord.utils.find(lambda r: r.name == 'FBS Conference Commissioner', message.guild.roles)
        fcs_commissioner = discord.utils.find(lambda r: r.name == 'FCS Conference Commissioner', message.guild.roles)
        if message.guild is not None and message.author is discord.Member:
            roles = message.author.roles
            if nfcaa_office in roles or fbs_commissioner in roles or fcs_commissioner in roles:
                if message_content.startswith('$start_games'):
                    if config_data['week_run'] == "YES":
                        await message.channel.send("The games have already been started for this week, please verify you want to start and then reset this by using command $reset_week before starting the games again")
                    else:
                        await handle_start_games_command(r, message)
                        config_data['week_run'] = "YES"
                elif message_content.startswith('$reset_week'):
                    await handle_reset_week_command(config_data, message)
                
    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token)