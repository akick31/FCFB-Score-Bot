import praw
import discord
import json
from parse_game_data import *
from win_probability import *
from scorebug_drawer import *


with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)


"""
Get information to make a post for ongoing games on Reddit

"""


async def get_ongoing_game_information(message, submission, home_vegas_odds, away_vegas_odds, home_team, away_team, home_score, away_score):
    # Get win probability
    cur_possession = parse_possession(submission.selftext)
    win_probability_result = get_in_game_win_probability(home_team, away_team)
    offense_win_probability = win_probability_result[1]
    last_play_possession_change = win_probability_result[2]

    if cur_possession == home_team and last_play_possession_change is False:
        home_win_probability = offense_win_probability
    elif cur_possession == home_team and last_play_possession_change is True:
        home_win_probability = 100 - offense_win_probability
    else:
        home_win_probability = 100 - offense_win_probability
    away_win_probability = 100 - home_win_probability

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

    await craft_ongoing_game_comment(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, home_vegas_odds, home_team, away_team, home_score, away_score, home_win_probability, waiting_on)


"""
Make posts for ongoing games on Reddit

"""


async def craft_ongoing_game_comment(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, vegas_odds, home_team, away_team, home_score, away_score, home_win_probability, waiting_on):
    odds = round(vegas_odds * 2) / 2
    if odds == 0:
        odds_post = "Push"
    elif odds > 0:
        odds_post = home_team + " +" + str(odds)
    else:
        odds_post = home_team + " " + str(odds)

    win_post = "Each team has a 50% chance to win\n"
    if int(home_win_probability) >= 50:
        win_post = home_team + " has a " + str(int(home_win_probability)) + "% chance to win\n"
    elif int(home_win_probability) < 50:
        win_post = away_team + " has a " + str(100 - int(home_win_probability)) + "% chance to win\n"

    home_record = parse_home_record(submission.title)
    away_record = parse_away_record(submission.title)

    embed = discord.Embed(title="**Game Information**", color=0x005EB8)
    embed.add_field(name="**Watch**", value="[Game Thread](" + submission.url + ")", inline=False)
    embed.add_field(name="**Spread**", value=odds_post, inline=False)
    embed.add_field(name="**Win Probability**", value=win_post, inline=False)

    draw_scorebug(cur_clock, cur_down, cur_possession, cur_yard_line, odds, home_team, away_team,
                  home_score, away_score, waiting_on, home_record, away_record)

    with open('scorebug_new.png', 'rb') as fp:
        file = discord.File(fp, 'posted_scorebug.png')
        embed.set_image(url="attachment://posted_scorebug.png")

    embed.add_field(name="**Ball Location**", value=cur_yard_line, inline=False)
    await message.channel.send(embed=embed, file=file)

    print("Comment posted for " + home_team + " vs " + away_team + "\n")


"""
Get the home record from the title
"""


def parse_home_record(title):
    if "@" in title:
        for item in title.split("@")[1].split(" "):
            if "(" in item and "-" in item:
                return item
    return None
        

"""
Get the away record from the title
"""


def parse_away_record(title):
    if "@" in title:
        for item in title.split("@")[0].split(" "):
            if "(" in item and "-" in item:
                return item
    return None

"""
Make posts for games that went final on Reddit

"""


async def craft_game_final_score_comment(message, submission, home_team, away_team, vegas_odds, home_score, away_score,
                                         home_record, away_record):
    if vegas_odds == "NONE":
        odds = ""
    else:
        odds = round(vegas_odds * 2) / 2
        number_odds = odds
        if odds == 0:
            odds = "Push"
        elif odds > 0:
            odds = "+" + str(odds)

    embed = discord.Embed(title="**Post Game Information**", color=0x005EB8)
    draw_final_scorebug(odds, home_team, away_team, home_score, away_score, home_record, away_record)

    with open('scorebug_final.png', 'rb') as fp:
        file=discord.File(fp, 'posted_final_scorebug.png')
        embed.set_image(url="attachment://posted_final_scorebug.png")

    embed.add_field(name="**Discuss**", value="[Post Game Thread](" + submission.url + ")", inline=False)
    await message.channel.send(embed=embed, file=file)

    print("Comment posted for " + home_team + " vs " + away_team + "\n")


"""
Login to reddit

"""


def login_reddit():
    r = praw.Reddit(user_agent=config_data['user_agent'],
                    client_id=config_data['client_id'],
                    client_secret=config_data['client_secret'],
                    username=config_data['username'],
                    password=config_data['password'],
                    subreddit=config_data['subreddit'])
    return r