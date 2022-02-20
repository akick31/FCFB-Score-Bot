#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 20:24:10 2020

@author: apkick
"""


"""
Parse the team that the game is waiting 

"""


def parse_waiting_on(submission_body, home_user, away_user, home_team, away_team):
    if "Waiting on a response from" in submission_body:
        user = submission_body.split("Waiting on a response from")[1].split("to this")[0].strip()
        if user == home_user:
            return home_team
        elif user == away_user:
            return away_team


"""
Parse the home team user from the game thread

"""


def parse_home_user(submission_body):
    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        home_user = submission_body.split("___")[0].split("\n")[13].split("|")[1].strip()
    else:
        home_user = submission_body.split("___")[0].split("\n")[11].split("|")[1].strip()
    return home_user


"""
Parse the away team user from the game thread

"""


def parse_away_user(submission_body):
    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        away_user = submission_body.split("___")[0].split("\n")[12].split("|")[1].strip()
    else:
        away_user = submission_body.split("___")[0].split("\n")[10].split("|")[1].strip()
    return away_user


"""
Parse the quarter from the game thread

"""


def parse_quarter(submission_body):
    if len(submission_body.split("___")) == 7:
        quarter = submission_body.split("___")[4].split("\n")[4].split("|")[1].split(" ")[0]
    else:
        quarter = submission_body.split("___")[4].split("\n")[3].split("|")[1].split(" ")[0]
    if quarter == "1":
        return "1Q"
    elif quarter == "2":
        return "2Q"
    elif quarter == "3":
        return "3Q"
    elif quarter == "4":
        return "4Q" 
    else:
        return "OT"


"""
Parse the yard line from the game thread

"""


def parse_yard_line(submission_body):
    if len(submission_body.split("___")) == 7:
        # Get the time
        yard_line_field = submission_body.split("___")[4].split("\n")[4].split("|")[3]
        if yard_line_field.strip() != "50":
            side_of_field = yard_line_field.split("]")[0].split("[")[1]
            yard_line = yard_line_field.split("[")[0]
        else:
            return "50"
    else:
        yard_line_field = submission_body.split("___")[3].split("\n")[4].split("|")[3]
        if yard_line_field.strip() != "50":
            side_of_field = yard_line_field.split("]")[0].split("[")[1]
            yard_line = yard_line_field.split("[")[0]
        else:
            return "50"
    return side_of_field + " " + yard_line  


"""
Parse the down from the game thread

"""


def parse_down(submission_body):
    if len(submission_body.split("___")) == 7:
        # Get the time
        down = submission_body.split("___")[4].split("\n")[4].split("|")[2]
    else:
        down = submission_body.split("___")[3].split("\n")[4].split("|")[2]
    return down


"""
Parse what team has the ball from the game thread

"""


def parse_possession(submission_body):
    possession = "home"
    possession = submission_body.split("___")[4].split("\n")[4].split("|")[4].split("]")[0].split("[")[-1]
    return possession


"""
Parse the time from the game thread

"""


def parse_time(submission_body):
    if(len(submission_body.split("___")) == 7):
        # Get the time
        time = submission_body.split("___")[4].split("\n")[4].split("|")[0]
    else:
        time = submission_body.split("___")[4].split("\n")[3].split("|")[0]
    return time 


"""
Parse the home score from the game thread

"""


def parse_home_score(submission_body):
    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team_score = scoreboard[4].split("**")[1]
        
    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team_score = scoreboard[4].split("**")[1]
        
    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        home_team_score = scoreboard[4].split("**")[1]
        
    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        home_team_score = scoreboard[4].split("**")[1]
        
    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        home_team_score = scoreboard[3].split("**")[1]
        
    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        home_team_score = scoreboard[2].split(" | ")[-1]
        
    return home_team_score


"""
Parse the away score from the game thread

"""


def parse_away_score(submission_body):
    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team_score = scoreboard[5].split("**")[1]
        
    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team_score = scoreboard[5].split("**")[1]
        
    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        away_team_score = scoreboard[5].split("**")[1]
        
    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        away_team_score = scoreboard[5].split("**")[1]
        
    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        away_team_score = scoreboard[4].split("**")[1]
        
    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        away_team_score = scoreboard[3].split(" | ")[-1]
    return away_team_score
    

"""
Parse the home team from the game thread

"""


def parse_home_team(submission_body):
    home_team = "blank"
    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        home_team = scoreboard[3].split("]")[0]
        home_team = home_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        home_team = scoreboard[2].split("]")[0]
        home_team = home_team.replace('[', '')
    return home_team


"""
Parse the away team from the game thread

"""


def parse_away_team(submission_body):
    away_team = "blank"
    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        away_team = scoreboard[4].split("]")[0]
        away_team = away_team.replace('[', '')
        
    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        away_team = scoreboard[3].split("]")[0]
        away_team = away_team.replace('[', '')

    return away_team
