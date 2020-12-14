#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 20:24:10 2020

@author: apkick
"""

"""
Parse the team that the game is waiting 

"""
def parseWaitingOn(submissionbody, homeUser, awayUser, homeTeam, awayTeam):
    if("Waiting on a response from" in submissionbody):
        user = submissionbody.split("Waiting on a response from")[1].split("to this")[0].strip()
        if(user == homeUser):
            return homeTeam
        elif(user == awayUser):
            return awayTeam
    
"""
Parse the home team user from the game thread

"""    
def parseHomeUser(submissionbody):
    homeUser = submissionbody.split("___")[0].split("\n")[13].split("|")[1].strip()
    return homeUser
    
"""
Parse the away team user from the game thread

"""    
def parseAwayUser(submissionbody):
    awayUser = submissionbody.split("___")[0].split("\n")[12].split("|")[1].strip()
    return awayUser


"""
Parse the quarter from the game thread

"""
def parseQuarter(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        quarter = submissionbody.split("___")[4].split("\n")[4].split("|")[1].split(" ")[0]
    else:
        quarter = submissionbody.split("___")[4].split("\n")[3].split("|")[1].split(" ")[0]
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
def parseYardLine(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        # Get the time
        yardLineField = submissionbody.split("___")[4].split("\n")[4].split("|")[3]
        if(yardLineField.strip() != "50"):
            sideOfField = yardLineField.split("]")[0].split("[")[1]
            yardLine = yardLineField.split("[")[0]
        else:
            return "50"
    else:
        yardLineField = submissionbody.split("___")[3].split("\n")[4].split("|")[3]
        if(yardLineField.strip() != "50"):
            sideOfField = yardLineField.split("]")[0].split("[")[1]
            yardLine = yardLineField.split("[")[0]
        else:
            return "50"
    return sideOfField + " " + yardLine  
 
"""
Parse the down from the game thread

"""
def parseDown(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        # Get the time
        down = submissionbody.split("___")[4].split("\n")[4].split("|")[2]
    else:
        down = submissionbody.split("___")[3].split("\n")[4].split("|")[2]
    return down

"""
Parse what team has the ball from the game thread

"""  
def parsePossession(submissionbody):
    possession = "home"
    possession = submissionbody.split("___")[4].split("\n")[4].split("|")[4].split("]")[0].split("[")[-1]
    #Iterate through playlist file
    #with open('data.txt', 'r') as csvfile:
    #    reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n')
    #    for row in reader:
    #        if(row[0] != '--------------------------------------------------------------------------------'):
    #            possession = row[5]
    return possession
    
"""
Parse the time from the game thread

"""
def parseTime(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        # Get the time
        time = submissionbody.split("___")[4].split("\n")[4].split("|")[0]
    else:
        time = submissionbody.split("___")[4].split("\n")[3].split("|")[0]
    return time 
    
"""
Parse the home score from the game thread

"""
def parseHomeScore(submissionbody):
    # Handle various different thread formats
    if(len(submissionbody.split("___")) == 7):
        scoreboard = submissionbody.split("___")[5].split("\n")
        homeTeamScore = scoreboard[4].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 6):
        scoreboard = submissionbody.split("___")[5].split("\n")
        homeTeamScore = scoreboard[4].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 5):
        scoreboard = submissionbody.split("___")[4].split("\n")
        homeTeamScore = scoreboard[4].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 4):
        scoreboard = submissionbody.split("___")[3].split("\n")
        homeTeamScore = scoreboard[4].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 3):
        scoreboard = submissionbody.split("___")[2].split("\n")
        homeTeamScore = scoreboard[3].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        homeTeamScore = scoreboard[2].split(" | ")[-1]
        
    return homeTeamScore

"""
Parse the away score from the game thread

"""
def parseAwayScore(submissionbody):
    # Handle various different thread formats
    if(len(submissionbody.split("___")) == 7):
        scoreboard = submissionbody.split("___")[5].split("\n")
        awayTeamScore = scoreboard[5].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 6):
        scoreboard = submissionbody.split("___")[5].split("\n")
        awayTeamScore = scoreboard[5].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 5):
        scoreboard = submissionbody.split("___")[4].split("\n")
        awayTeamScore = scoreboard[5].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 4):
        scoreboard = submissionbody.split("___")[3].split("\n")
        awayTeamScore = scoreboard[5].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 3):
        scoreboard = submissionbody.split("___")[2].split("\n")
        awayTeamScore = scoreboard[4].split("**")[1]
        
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        awayTeamScore = scoreboard[3].split(" | ")[-1]
    return awayTeamScore
    

"""
Parse the home team from the game thread

"""
def parseHomeTeam(submissionbody):
    homeTeam = "blank"
    # Handle various different thread formats
    if(len(submissionbody.split("___")) == 7):
        scoreboard = submissionbody.split("___")[5].split("\n")
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 6):
        scoreboard = submissionbody.split("___")[5].split("\n")
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 5):
        scoreboard = submissionbody.split("___")[4].split("\n")
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 4):
        scoreboard = submissionbody.split("___")[3].split("\n")
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 3):
        scoreboard = submissionbody.split("___")[2].split("\n")
        homeTeam = scoreboard[3].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        homeTeam = scoreboard[2].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
    return homeTeam

"""
Parse the away team from the game thread

"""
def parseAwayTeam(submissionbody):
    awayTeam = "blank"
    # Handle various different thread formats
    if(len(submissionbody.split("___")) == 7):
        scoreboard = submissionbody.split("___")[5].split("\n")
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 6):
        scoreboard = submissionbody.split("___")[5].split("\n")
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 5):
        scoreboard = submissionbody.split("___")[4].split("\n")
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 4):
        scoreboard = submissionbody.split("___")[3].split("\n")
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 3):
        scoreboard = submissionbody.split("___")[2].split("\n")
        awayTeam = scoreboard[4].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
        
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        awayTeam = scoreboard[3].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
    return awayTeam