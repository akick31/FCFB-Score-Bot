import praw
import json
from parse_game_data import *
from win_probability import *


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

    # If home team is winning or the score is tied
    if int(home_score) > int(away_score) or int(home_score) == int(away_score):
        await craft_ongoing_game_comment(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, home_vegas_odds, home_team, away_team, home_score, away_score, home_win_probability, waiting_on)
    # If the home team is losing
    elif int(home_score) < int(away_score):
        await craft_ongoing_game_comment(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, away_vegas_odds, away_team, home_team, away_score, home_score, away_win_probability, waiting_on)


"""
Make posts for ongoing games on Reddit

"""


async def craft_ongoing_game_comment(message, submission, cur_clock, cur_down, cur_possession, cur_yard_line, vegas_odds, team, opponent_team, score, opponent_score, cur_win_probability, waiting_on):
    odds = round(vegas_odds * 2) / 2
    if odds == 0:
        odds = "Push"
    elif odds > 0:
        odds = "+" + str(odds)
    post = "**" + cur_clock + " | " + opponent_team + " " + opponent_score + " " + team + " " + score + " (" + str(odds) + ")** \n"
    yard_post = cur_down + " | :football: " + cur_possession + " | " + cur_yard_line + "\n"
    win_post = "Each team has a 50% chance to win\n"
    if int(cur_win_probability) >= 50:
        win_post = team + " has a " + str(int(cur_win_probability)) + "% chance to win\n"
    elif int(cur_win_probability) < 50:
        win_post = opponent_team + " has a " + str(100-int(cur_win_probability)) + "% chance to win\n"
    waiting_on_post = "Waiting on " + waiting_on + " for a number\n"
    await message.channel.send(post + yard_post + win_post + waiting_on_post + submission.url + "\n")
    print("Comment posted for " + team + " vs " + opponent_team + "\n")


"""
Make posts for games that went final on Reddit

"""


async def craft_game_final_score_comment(message, team, opponent_team, vegas_odds, score, opponent_score):
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
    print("Comment posted for " + team + " vs " + opponent_team + "\n")


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