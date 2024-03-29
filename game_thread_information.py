import asyncpraw
import requests
import datetime
from parse_game_data import *
from handle_dates import *

with open('season_information.json', 'r') as config_file:
    season_info_data = json.load(config_file)

"""
Gather the game thread information

@author: apkick
"""


"""
Search for a game thread based on what the user requests, searches for two teams in a time span range
based on what season the user wants to search. Season 4 is the default if they do not specify a season

"""


def search_for_request_game_thread(submission, home_team, away_team, season, request, postseason, game_time):
    if request == "$score":
        link_flair = ["blank", "Game Thread", "Post Game Thread"]
    # Else the request is for the game plots
    else:
        link_flair = ["Game Thread", "Week 10 Game Thread", "Week 9 Game Thread"]

    away = "blank"
    home = "blank"

    # Get home/away teams
    if submission.link_flair_text in link_flair:
        away = parse_away_team(submission.selftext).lower()
        home = parse_home_team(submission.selftext).lower()
        print(submission.title)

    if (submission.link_flair_text in link_flair and season in season_info_data['seasons']
            and check_if_in_season(season, game_time) and "MIAA" not in submission.title
            and ((home_team == home or home_team == away) and (away_team == home or away_team == away))):
        if postseason == 1 and check_if_in_postseason(season, game_time):
            return submission
        elif postseason == 0 and check_if_in_regular_season(season, game_time):
            return submission

    return "NONE"


"""
Parse the data from the Github Gist into data.txt

"""


def parse_data_from_github(github_url):
    # Parse data from the github url
    url = github_url + "/raw"
    req = requests.get(url)
    
    # Remove the very first line from the data
    data = ""
    flag = 0
    for character in req.text:
        if flag == 0 and character == "0":
            data = data + "0"
            flag = 1
        elif flag == 1:
            data = data + character 
    if data.find('--------------------------------------------------------------------------------\n') >= 0:
        data = data.replace('--------------------------------------------------------------------------------\n', '')
    return data


"""
Iterate through Reddit to find the game threads

"""


def search_for_game_thread(r, home_team, away_team, season, request, postseason):
    if postseason != 0:
        search_item = "\"Game Thread\" \"Bowl\" \"Playoffs\" \"" + home_team + "\" \"" + away_team + "\""
    else:
        search_item = "\"Game Thread\" \"" + home_team + "\" \"" + away_team + "\""
    print("Search Query: " + search_item)

    for submission in r.subreddit("FakeCollegeFootball").search(search_item, sort='new'):
        # Get game thread submission day
        game_time = datetime.datetime.fromtimestamp(int(submission.created_utc))
        home_team = home_team.lower()
        away_team = away_team.lower()
        game_thread = search_for_request_game_thread(submission, home_team, away_team, season, request, postseason, game_time)
        if game_thread != "NONE":
            print("\n" + game_thread.url)
            return game_thread
    return "NONE"


"""
Iterate through Reddit to find the game thread and return a dictionary of the two teams in that game, with the 
1 value being the team you're looking for, 2 value being their opponent

"""


def search_for_team_game_thread(r, team):
    for submission in r.subreddit("FakeCollegeFootball").search(team, sort='new'):
        if submission.link_flair_text == "Game Thread":
            away = parse_away_team(submission.selftext)
            home = parse_home_team(submission.selftext)
        if submission.link_flair_text == "Game Thread" and (team.lower() == home.lower() or team.lower() == away.lower()):
            if team.lower() == home.lower():
                return {1: home, 2: away}
            elif team.lower() == away.lower():
                return {1: away, 2: home}
    return {1: "NONE", 2: "NONE"}


"""
Parse the Gist url from the game thread

"""


def parse_url_from_game_thread(submission_body, season):
    if "github" not in submission_body and "pastebin" not in submission_body:
        return "NO PLAYS"
    elif "Waiting on a response" in submission_body:
        split_list = submission_body.split("Waiting on")[0].split("[Plays](")
        num_items = len(split_list) - 1
        return split_list[num_items].split(")")[0]
    else:
        split_list = submission_body.split("#Game complete")[0].split("[Plays](")
        num_items = len(split_list) - 1
        return split_list[num_items].split(")")[0]


"""
Save the Github Gist data into data.txt

"""


def save_github_data(submission_body, season):
    url = parse_url_from_game_thread(submission_body, season)
    if url != "NO PLAYS":
        data = parse_data_from_github(url)
        text_file = open("data.txt", "w")
        text_file.write(data)
        text_file.close()
    return url
