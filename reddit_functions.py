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
    offense_win_probability = get_in_game_win_probability(home_team, away_team)
    if cur_possession == home_team:
        home_win_probability = offense_win_probability
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

    post = ("**__Game Information__**\n**Win Probability:** " + win_post + "**Spread**: " + odds_post
            + "\n**Ball Location:** " + cur_yard_line)

    draw_scorebug(cur_clock, cur_down, cur_possession, cur_yard_line, odds, home_team, away_team,
                  home_score, away_score, waiting_on, home_record, away_record)

    with open('scorebug_new.png', 'rb') as fp:
        await message.channel.send(post, file=discord.File(fp, 'posted_scorebug.png'))

    await message.channel.send("**Watch:** " + submission.url)

    print("Comment posted for " + home_team + " vs " + away_team + "\n")


"""
Get the home record from the title
"""


def parse_home_record(title):
    for item in title.split("@")[1].split(" "):
        if "(" in item and "-" in item:
            return item
        

"""
Get the away record from the title
"""


def parse_away_record(title):
    for item in title.split("@")[0].split(" "):
        if "(" in item and "-" in item:
            return item


"""
Make posts for games that went final on Reddit

"""


async def craft_game_final_score_comment(message, submission, home_team, away_team, vegas_odds, home_score, away_score):
    if vegas_odds == "NONE":
        odds = ""
    else:
        odds = round(vegas_odds * 2) / 2
        number_odds = odds
        if odds == 0:
            odds = "Push"
        elif odds > 0:
            odds = "+" + str(odds)

    draw_final_scorebug(odds, home_team, away_team, home_score, away_score)

    with open('scorebug_final.png', 'rb') as fp:
        await message.channel.send(file=discord.File(fp, 'posted_final_scorebug.png'))

    await message.channel.send("**Post Game Thread:** " + submission.url)

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