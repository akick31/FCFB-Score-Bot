#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import matplotlib.pyplot as plt
import csv
import requests
import praw
import discord
import time
import gspread
import math
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands
from scipy.stats import norm

"""
Program that posts game data to Discord. Heroku email is FCFBScoreBot@gmail.com

@author: Andrew Kicklighter
"""

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('FCFBRollCallBot-2d263a255851.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZFi4MqxWX84-VdIiWjJmuvB8f80lfKNkffeKcdJKtAU/edit#gid=1733685321')
fbsworksheet = sh.worksheet("Season 4 Rankings (All-Time)")

sh2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Us7nH-Xh1maDyRoVzwEh2twJ47UroXdCNZWSFG28cmg/edit#gid=0')
fcsworksheet = sh2.worksheet("FCSElo")

sh3 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1-1Fte7S8kXy8E-GY7c3w00vrVcvbY87MWHJln8Ev4S0/edit?usp=sharing')
colorworksheet = sh3.worksheet("Sheet1")

subreddit = "FakeCollegeFootball"

    
# Login to Reddit
def loginReddit():
    r = praw.Reddit(user_agent='ScoreboardBot by /u/akick31',
                    client_id='mbxqsh9-BGzlow',
                    client_secret='DUh4hWoT3QvsJnk3ctepVjxbDWo',
                    username='FCFBScoreBot',
                    password='goodbyerhule',
                    subreddit='FakeCollegeFootball')
    return r   
    
# Login to Discord and run the bot
def loginDiscord(r):
    token = 'NzA4ODIzNzc3NDI0NzAzNTE5.Xrc9tA.vcsJTLYrVqomAFSnLwY09BlXzYE'

    client = discord.Client()

    @client.event
    async def on_message(message):
        global postEdited, changeIndex
        
        if(message.content.startswith('$score') or message.content.startswith('$Score')):
            if("vs" in message.content):
                if(message.content.startswith('$score')):
                   teams = message.content.split("$score")[1]
                elif(message.content.startswith('$Score')):
                    teams = message.content.split("$Score")[1]

                hometeam = teams.split("vs")[0]
                awayteam = teams.split("vs")[1]
                
                hometeam = hometeam.strip()
                awayteam = awayteam.strip()
                
                # Parse the season number from string
                season = "S4"
                postseason = 0
                    
                if(("S1" in awayteam or "S2" in awayteam or "S3" in awayteam or "S4" in awayteam)
                   or ("s1" in awayteam or "s2" in awayteam or "s3" in awayteam or "s4" in awayteam)):
                    teamsplit = awayteam.split(" ")
                    i = 0
                    for split in teamsplit:
                        if(("S1" in split or "S2" in split or "S3" in split or "S4" in split)
                           or ("s1" in split or "s2" in split or "s3" in split or "s4" in split)):
                            season = teamsplit[i]
                        if("postseason" in split or "Postseason" in split):
                            postseason = 1
                        i = i + 1
                    awayteam = awayteam.split(season)[0] 
                    awayteam = awayteam.strip()
                    
                
                await message.channel.send("Looking for the game thread...")
                print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + hometeam + " vs " + awayteam)
                
                if(hometeam.find('A&M') >= 0 or hometeam.find('a&m') >= 0):
                    hometeam = hometeam.replace('&', '&amp;')
                if(awayteam.find('A&M') >= 0 or awayteam.find('a&m') >= 0):
                    awayteam = awayteam.replace('&', '&amp;')
                if(hometeam == 'Miami' or hometeam == 'miami'):
                    hometeam = 'miami (fl)'
                if(awayteam == 'Miami' or awayteam == 'miami'):
                    awayteam = 'miami (fl)'
                
                submission = searchForGameThread(r, hometeam, awayteam, season, "$score", postseason)
                if(submission == "NONE"):
                    await message.channel.send("No game thread found.")
                else:
                    print("GAME THREAD FOUND")
                    
                    url = parseURLFromGameThread(submission.selftext, season)
                    if(url != "NO PLAYS"):
                        data = parseDataFromGithub(url)
                        text_file = open("data.txt", "w")
                        text_file.write(data)
                        text_file.close()
                    hometeam = parseHomeTeam(submission.selftext)
                    awayteam = parseAwayTeam(submission.selftext)
                    
                    # Fix mistakes in naming
                    if(hometeam.find('amp;') >= 0):
                        hometeam = hometeam.replace('amp;', '')
                    if(awayteam.find('amp;') >= 0):
                        awayteam = awayteam.replace('amp;', '')
                        
                    # Hardcode to fix inconsistencies in stat sheets
                    if(hometeam == "UMass"):
                        hometeam = "Massachusetts"
                    elif(awayteam == "UMass"):
                        awayteam = "Massachusetts"
                        
                    if(hometeam == "Southern Mississippi"):
                        hometeam = "Southern Miss"
                    elif(awayteam == "Southern Mississippi"):
                        awayteam = "Southern Miss"
                        
                    if(hometeam == "Miami (FL)"):
                        hometeam = "Miami"
                    elif(awayteam == "Miami (FL)"):
                        awayteam = "Miami"
                    
                    if(hometeam == "Miami (OH)"):
                        hometeam = "Miami, OH"
                    elif(awayteam == "Miami (OH)"):
                        awayteam = "Miami, OH"
                        
                    colorDictionary = getColorData()
                    teamcolorcolumn = colorDictionary[1]
                    colordatacolumn = colorDictionary[2]
                    eloDictionary = getEloData()
                    teamelocolumn = eloDictionary[1]
                    elodatacolumn = eloDictionary[2]
                        
                    homecolor = getColor(hometeam, teamcolorcolumn, colordatacolumn)
                    awaycolor = getColor(awayteam, teamcolorcolumn, colordatacolumn)
                      
                    # Get the vegas odds
                    homeelo = getElo(hometeam, teamelocolumn, elodatacolumn)
                    awayelo = getElo(awayteam, teamelocolumn, elodatacolumn)
                    homeVegasOdds = getHomeVegasOdds(homeelo, awayelo)
                    awayVegasOdds = getAwayVegasOdds(homeelo, awayelo)
                    
                    # Get the score
                    homescore = parseHomeScore(submission.selftext)
                    awayscore = parseAwayScore(submission.selftext)
                    
                    #Work with new gist
                    if(season == "S4"):
                        # Get win probability
                        curPossession = parsePossession(submission.selftext)
                        possessingTeamProbability = getCurrentWinProbabilityNew(homeVegasOdds, awayVegasOdds)
                        if(curPossession == hometeam):
                            curHomeWinProbability = possessingTeamProbability
                        else:
                            curHomeWinProbability = 100-possessingTeamProbability
                        curAwayWinProbability = 100-curHomeWinProbability
                        # Get other game data
                        curYardLine = parseYardLine(submission.selftext)
                        curQuarter = parseQuarter(submission.selftext)
                        curDown = parseDown(submission.selftext)
                        curTime = parseTime(submission.selftext)
                        # If game is final, display that
                        if(curQuarter == "OT"):
                            curClock = "OT"
                        else:
                            curClock = str(curTime) + " " + str(curQuarter) 
                        
                    if("Game complete" in submission.selftext):
                        if(season == "S4"):
                            if(int(homescore) > int(awayscore) or int(homescore) == int(awayscore)):
                                odds = round(homeVegasOdds * 2) / 2
                                numberOdds = odds
                                if(odds == 0):
                                    odds = "Push"
                                elif(odds > 0):
                                    odds = "+" + str(odds)
                                post = "**FINAL | " + hometeam + " defeated " + awayteam + " " + homescore + "-" + awayscore + "**\n"
                                if(int(numberOdds) > 0):
                                    await message.channel.send(post + "UPSET! " + hometeam + " was underdogs at " + str(odds) + " and won!")
                                if(int(numberOdds) < 0 and ((int(awayscore) - int(homescore)) > numberOdds)):
                                    await message.channel.send(post + awayteam + " beat the spread listed at " + str(odds))
                                elif(int(numberOdds) < 0 and ((int(awayscore) - int(homescore)) < numberOdds)):
                                    print(numberOdds)
                                    await message.channel.send(post + hometeam + " covered the spread listed at " + str(odds))
                                if(int(numberOdds) == 0 or ((int(awayscore) - int(homescore)) == numberOdds)):
                                    await message.channel.send(post + "This game was a push!")
                            elif(int(homescore) < int(awayscore)):
                                odds = round(awayVegasOdds * 2) / 2
                                numberOdds = odds
                                if(odds == 0):
                                    odds = "Push"
                                elif(odds > 0):
                                    odds = "+" + str(odds)
                                post = "**FINAL | " + awayteam + " defeated " + hometeam + " " + awayscore + "-" + homescore + "**\n"
                                if(int(numberOdds) > 0):
                                    await message.channel.send(post + "UPSET! " + awayteam + " was underdogs at " + str(odds) + " and won!")
                                if(int(numberOdds) < 0 and ((int(homescore) - int(awayscore)) > numberOdds)):
                                    await message.channel.send(post + hometeam + " beat the spread listed at " + str(odds))
                                elif(int(numberOdds) < 0 and ((int(homescore) - int(awayscore)) < numberOdds)):
                                    await message.channel.send(post + awayteam + " covered the spread listed at " + str(odds))
                                if(int(numberOdds) == 0 or ((int(homescore) - int(awayscore)) == numberOdds)):
                                    await message.channel.send(post + "This game was a push!")   
                        else:
                            post = "blank"
                            if(int(homescore) > int(awayscore)):
                                post = "**FINAL | " + hometeam + " defeated " + awayteam + " " + homescore + "-" + awayscore + "**\n"
                            else:
                                post = "**FINAL | " + awayteam + " defeated " + hometeam + " " + awayscore + "-" + homescore + "**\n"
                            await message.channel.send(post)
                    else:
                        if(season == "S4"):
                            # If home team is winning or the score is tied
                            if(int(homescore) > int(awayscore) or int(homescore) == int(awayscore)):
                                odds = round(homeVegasOdds * 2) / 2
                                if(odds == 0):
                                    odds = "Push"
                                elif(odds > 0):
                                    odds = "+" + str(odds)
                                post = "**" + curClock +  " | " + awayteam + " " + awayscore + " " + hometeam + " " + homescore + " (" + str(odds) + ")** \n"
                                yardPost = curDown + " | :football: " + curPossession + " | " + curYardLine + "\n"
                                winPost = "Each team has a 50% chance to win\n"
                                if(int(curHomeWinProbability) > int(curAwayWinProbability)):
                                    winPost = hometeam + " has a " + str(int(curHomeWinProbability)) + "% chance to win\n"
                                elif(int(curHomeWinProbability) < int(curAwayWinProbability)):
                                    winPost = awayteam + " has a " + str(int(curAwayWinProbability)) + "% chance to win\n"
                                await message.channel.send(post + yardPost + winPost)   
                            #If the home team is losing
                            elif(int(homescore) < int(awayscore)):
                                odds = round(awayVegasOdds * 2) / 2
                                if(odds == 0):
                                    odds = "Push"
                                elif(odds > 0):
                                    odds = "+" + str(odds)
                                post = "**" + curClock + " | " + awayteam + " " + awayscore  + " (" + str(odds) + ") " + hometeam + " " + homescore + "**\n"
                                yardPost = curDown + " | :football: " + curPossession + " | " + curYardLine + "\n"
                                winPost = "Each team has a 50% chance to win \n"
                                if(int(curHomeWinProbability) > int(curAwayWinProbability)):
                                    winPost = hometeam + " has a " + str(int(curHomeWinProbability)) + "% chance to win\n"
                                elif(int(curHomeWinProbability) < int(curAwayWinProbability)):
                                    winPost = awayteam + " has a " + str(int(curAwayWinProbability)) + "% chance to win\n"
                                await message.channel.send(post + yardPost + winPost)
                        else:
                            post = "blank"
                            if(int(homescore) > int(awayscore)):
                                post = "**FINAL | " + hometeam + " defeated " + awayteam + " " + homescore + "-" + awayscore + "**\n"
                            else:
                                post = "**FINAL | " + awayteam + " defeated " + hometeam + " " + awayscore + "-" + homescore + "**\n"
                            await message.channel.send(post)
                  
            else: 
                await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")
        
        elif(message.content.startswith('$plot') or message.content.startswith('$Plot')):
            if("vs" in message.content):
                if(message.content.startswith('$plot')):
                   teams = message.content.split("$plot")[1]
                elif(message.content.startswith('$Plot')):
                    teams = message.content.split("$Plot")[1]

                hometeam = teams.split("vs")[0]
                awayteam = teams.split("vs")[1]
                
                hometeam = hometeam.strip()
                awayteam = awayteam.strip()
                
                # Parse the season number from string
                season = "S4"
                postseason = 0
                if(("S1" in awayteam or "S2" in awayteam or "S3" in awayteam or "S4" in awayteam)
                   or ("s1" in awayteam or "s2" in awayteam or "s3" in awayteam or "s4" in awayteam)):
                    teamsplit = awayteam.split(" ")
                    i = 0
                    for split in teamsplit:
                        if(("S1" in split or "S2" in split or "S3" in split or "S4" in split)
                           or ("s1" in split or "s2" in split or "s3" in split or "s4" in split)):
                            season = teamsplit[i]
                        if("postseason" in split or "Postseason" in split):
                            postseason = 1
                        i = i + 1
                    awayteam = awayteam.split(season)[0] 
                    awayteam = awayteam.strip()
                
                await message.channel.send("Looking for the game thread...")
                print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + hometeam + " vs " + awayteam)
                
                # Hard code inconsistencies 
                if(hometeam.find('A&M') >= 0 or hometeam.find('a&m') >= 0):
                    hometeam = hometeam.replace('&', '&amp;')
                if(awayteam.find('A&M') >= 0 or awayteam.find('a&m') >= 0):
                    awayteam = awayteam.replace('&', '&amp;')
                if(hometeam == 'Miami' or hometeam == 'miami'):
                    hometeam = 'miami (fl)'
                if(awayteam == 'Miami' or awayteam == 'miami'):
                    awayteam = 'miami (fl)'
                
                # Look for game thread
                submission = searchForGameThread(r, hometeam, awayteam, season, "$plot", postseason)
                if(submission == "NONE"):
                    await message.channel.send("No game thread found.")
                else:
                    print("GAME THREAD FOUND")
                    
                    # Parse data from url
                    url = parseURLFromGameThread(submission.selftext, season)
                    if(url != "NO PLAYS" and "github" in url):
                        data = parseDataFromGithub(url)
                        text_file = open("data.txt", "w")
                        text_file.write(data)
                        text_file.close()
                    elif(url != "NO PLAYS" and "pastebin" in url):
                        data = parseDataFromPastebin(url)
                        text_file = open("data.txt", "w")
                        text_file.write(data)
                        text_file.close()
                    hometeam = parseHomeTeam(submission.selftext)
                    awayteam = parseAwayTeam(submission.selftext)
                    
                    # Fix mistakes in naming
                    if(hometeam.find('amp;') >= 0):
                        hometeam = hometeam.replace('amp;', '')
                    if(awayteam.find('amp;') >= 0):
                        awayteam = awayteam.replace('amp;', '')
                        
                    # Hardcode to fix inconsistencies in stat sheets
                    if(hometeam == "UMass"):
                        hometeam = "Massachusetts"
                    elif(awayteam == "UMass"):
                        awayteam = "Massachusetts"
                        
                    if(hometeam == "Southern Mississippi"):
                        hometeam = "Southern Miss"
                    elif(awayteam == "Southern Mississippi"):
                        awayteam = "Southern Miss"
                        
                    if(hometeam == "Miami (FL)"):
                        hometeam = "Miami"
                    elif(awayteam == "Miami (FL)"):
                        awayteam = "Miami"
                        
                    if(hometeam == "Miami (OH)"):
                        hometeam = "Miami, OH"
                    elif(awayteam == "Miami (OH)"):
                        awayteam = "Miami, OH"
                        
                    colorDictionary = getColorData()
                    teamcolorcolumn = colorDictionary[1]
                    colordatacolumn = colorDictionary[2]
                    eloDictionary = getEloData()
                    teamelocolumn = eloDictionary[1]
                    elodatacolumn = eloDictionary[2]
                        
                    homecolor = getColor(hometeam, teamcolorcolumn, colordatacolumn)
                    awaycolor = getColor(awayteam, teamcolorcolumn, colordatacolumn)
                      
                    # Get the vegas odds
                    homeelo = getElo(hometeam, teamelocolumn, elodatacolumn)
                    awayelo = getElo(awayteam, teamelocolumn, elodatacolumn)
                    homeVegasOdds = getHomeVegasOdds(homeelo, awayelo)
                    awayVegasOdds = getAwayVegasOdds(homeelo, awayelo)
        
                    #Work with new gist
                    if(season == "S4"):
                        #If there is a GitHub URL as plays have been called
                        if(url != "NO PLAYS"):
                            # Iterate through the data and plot the graphs
                            iterateThroughNewData(hometeam, awayteam, homeVegasOdds, awayVegasOdds, homecolor, awaycolor)
                            
                            # Send score plot
                            with open('output.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                                
                            # Send the win probability plot
                            with open('outputWinProbability.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                        else:
                            await message.channel.send("No plays for the game found.")
                    else:
                        # Get game thread submission day
                        # submissionTime = datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
                        # year = int(submissionTime.split("-")[0])
                        # month = int(submissionTime.split("-")[1])
                        #day = int(submissionTime.split("-")[2].split(" ")[0])
                        #if(year > 2018 or (year == 2018 and month == 8 and day > 25) or (year == 2018 and month > 8)):
                        #    await message.channel.send("Iterating through old thread to generate plots...")
                        #    threadCrawler(hometeam, awayteam, homeVegasOdds, awayVegasOdds, homecolor, awaycolor, season, submission)
                            # Send score plot
                        #    with open('output.png', 'rb') as fp:
                        #        await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                                    
                        #    # Send the win probability plot
                        #    with open('outputWinProbability.png', 'rb') as fp:
                        #        await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                        #else:
                        await message.channel.send("This game is too old to plot the data. I can only plot Season IV games onward")
            else: 
                await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")
                
    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token)

# Calculate win probability
def calculateWinProbability(expectedPoints, quarter, time, teamScore, opponentScore, down, distance, yardLine, playType, vegasLine):  
    if(time == 0):
        time = 0.00001
    minutesInQuarter = time/60
    minutesRemaining = 28
    if(int(quarter) == 1):
        minutesRemaining = 28-(7-minutesInQuarter)
    elif(int(quarter) == 2):
        minutesRemaining = 21-(7-minutesInQuarter)
    elif(int(quarter) == 3):
        minutesRemaining = 14-(7-minutesInQuarter)
    elif(int(quarter) == 4):
        minutesRemaining = 7-(7-minutesInQuarter)
    else:
        minutesRemaining = 2
    
    if(minutesRemaining < 0):
        minutesRemaining = 0.01
        
    opponentMargin = opponentScore - teamScore
    opponentMargin = opponentMargin - expectedPoints
        
    stdDev = (13.45/math.sqrt((28/minutesRemaining)))
        
    winProbability = ((1-norm.cdf(((opponentMargin)+0.5),(-vegasLine*(minutesRemaining/28)),stdDev))
    +(0.5*(norm.cdf(((opponentMargin)+0.5), (-vegasLine*(minutesRemaining/28)), stdDev)
    - norm.cdf(((opponentMargin)-0.5),(-vegasLine*(minutesRemaining/28)), stdDev))))
    
    return winProbability
    
# Calculate the expected points
def calculateExpectedPoints(down, distance, yardLine, playType):
    if ((playType == 'PAT') or (playType == 'TWO_POINT')):
        return 0.952
        
    if ("KICKOFF" in playType):
        return 0 - calculateExpectedPoints(1, 10, 25, "EMPTY")
    
    intercept = 0
    slope = 0
    avgDist = 0
    distanceDiff = 0
    
    if(down == 1):
        avgDist = 10
        intercept = 2.43
        slope = 0.0478
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
    elif(down == 2):
        avgDist = 7.771
        intercept = 2.07
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
        slope = (distanceDiff * 0.0015) + 0.055
    elif(down == 3):
        avgDist = 6.902
        intercept = 1.38
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
        slope = (distanceDiff * 0.0015) + 0.055
    elif(down == 4):
        avgDist = 6.864
        intercept = -0.03
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
        slope = (distanceDiff * 0.0015) + 0.055
    
    if(down == 1):
        return intercept + (slope * (yardLine - 50)) + (((yardLine - 50) ** 3) / 100000) + max(0, (((1.65 ** 0.2) ** (yardLine - 94)) - 1) * (4))
    return intercept + (slope * (yardLine - 50)) + (((yardLine - 50) ** 3) / 100000) + max(0, (((1.65 ** 0.2) ** (yardLine - 94)) - 1) * (down/4))

 
# Get the current win probability for the current play
def getCurrentWinProbabilityNew(homeVegasOdds, awayVegasOdds):
    winProbability = []
    
    #Iterate through playlist file
    with open('data.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n')
        for row in reader:
            if(row[0] != '--------------------------------------------------------------------------------'):
                quarter = int(row[2])
                if(row[16] != ""):
                    time = int(row[3]) - int(row[17]) - int(row[16])
                else:
                    time = int(row[3]) 
                down = int(row[6])
                distance = int(row[7])
                if(row[15] != "" and int(row[15]) >= int(distance)):
                    down = 1
                    distance = 10
                elif(row[15] != "" and int(row[15]) < int(distance) and int(down) != 4):
                    down = int(down) + 1
                    distance = int(distance) - int(row[15])
                if(row[15] != ""):
                    yardLine = int(row[4]) + int(row[15])  
                else:
                    yardLine = int(row[4])
                playType = row[12]
                
                # Parse the win probability
                
                if((row[5] == "home" and (row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT")) 
                    or (row[5] == "away" and (row[14] == "TURNOVER" or row[14] == "KICK" or row[14] == "PUNT"))):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if((row[5] == "away" and (row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT")) 
                    or (row[5] == "home" and (row[14] == "TURNOVER" or row[14] == "KICK" or row[14] == "PUNT"))):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                # Handle if points were scored
                if(row[5] == "home" and row[14] == "TOUCHDOWN"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "PAT")
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[0]) + 6, int(row[1]), down, distance, yardLine, "PAT", homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "TOUCHDOWN"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "PAT")
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[1]) + 6, int(row[0]), down, distance, yardLine, "PAT", awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "FIELD GOAL"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[0]) + 3, int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "FIELD GOAL"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[1]) + 3, int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "PAT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[0]) + 1, int(row[1]), down, distance, yardLine, "KICKOFF", homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "PAT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[1]) + 1, int(row[0]), down, distance, yardLine, "KICKOFF", awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "TWO POINT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[0]) + 2, int(row[1]), down, distance, yardLine, "KICKOFF", homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "TWO POINT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[1]) + 2, int(row[0]), down, distance, yardLine, "KICKOFF", awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "SAFETY"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[0]), int(row[1]) + 2, down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "SAFETY"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[1]), int(row[0]) + 2, down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                
        return winProbability[-1]
    
# Iterate through the data for the plots
def iterateThroughNewData(hometeam, awayteam, homeVegasOdds, awayVegasOdds, homecolor, awaycolor):
    homeScore = []
    awayScore = []
    playNumber = []
    homeWinProbability = []
    awayWinProbability = []
    xList = []
    playCount = 1
    OTFlag = 0
    curHomeScore = 0
    curAwayScore = 0
    
    #Iterate through playlist file
    with open('data.txt', 'r+') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n')  
        rowCount = sum(1 for row in reader)
        currentRow = 1
        for row in reader:
            currentRow = currentRow + 1
            print(row)
            if(row[0] != '--------------------------------------------------------------------------------'):
                homeScore.append(int(row[0])) 
                awayScore.append(int(row[1]))
                curHomeScore = int(row[0])
                curAwayScore = int(row[1])
                playNumber.append(int(playCount))
                playCount = playCount + 1
                quarter = int(row[2])
                time = int(row[3])
                timemod = 4 - quarter 
                x = 1680 - (time + 420 * timemod)
                xList.append(x)
                if(quarter > 4):
                    OTFlag = 1
                down = int(row[6])
                distance = int(row[7])
                yardLine = int(row[4])       
                playType = row[12]
                
                expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)   
            
                if(rowCount == currentRow):
                    if(curHomeScore > curAwayScore):
                        homeWinProbability.append(100)
                        curHomeWinProbability = 100
                        awayWinProbability.append(0)
                        curAwayWinProbability = 0
                        break
                    elif(curHomeScore < curAwayScore):
                        awayWinProbability.append(100)
                        curAwayWinProbability = 100
                        homeWinProbability.append(0)
                        curHomeWinProbability = 0
                        break   
                # Parse the win probability
                if((row[5] == "home" and (row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT")) 
                    or (row[5] == "away" and (row[14] == "TURNOVER" or row[14] == "KICK" or row[14] == "PUNT"))):
                    curHomeWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    curAwayWinProbability = 100 - curHomeWinProbability
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(curAwayWinProbability)
                if((row[5] == "away" and (row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT")) 
                    or (row[5] == "home" and (row[14] == "TURNOVER" or row[14] == "KICK" or row[14] == "PUNT"))):
                    curAwayWinProbability = calculateWinProbability(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    curHomeWinProbability = 100 - curAwayWinProbability
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(curHomeWinProbability)  
            # Handle OT so that winner is at 100%
            if(rowCount == currentRow and OTFlag == 1):
                if(curHomeScore > curAwayScore):
                    homeWinProbability.append(100)
                    curHomeWinProbability = 100
                    awayWinProbability.append(0)
                    curAwayWinProbability = 0
                    homeScore.append(curHomeScore)
                    awayScore.append(curAwayScore)
                    playNumber.append(int(playCount))
                elif(curHomeScore < curAwayScore):
                    awayWinProbability.append(100)
                    curAwayWinProbability = 100
                    homeWinProbability.append(0)
                    curHomeWinProbability = 0
                    homeScore.append(curHomeScore)
                    awayScore.append(curAwayScore)
                    playNumber.append(int(playCount))
    
    #Plot score plot
    plotScorePlot(xList, hometeam, awayteam, homeScore, awayScore, playNumber, homecolor, awaycolor, OTFlag)
   
    #Plot win probability
    plotWinProbability(hometeam, awayteam, homeWinProbability, awayWinProbability, playNumber, homecolor, awaycolor)
    
    
# Plot the win probability for the game
def plotWinProbability(hometeam, awayteam, homeWinProbability, awayWinProbability, playNumber, homecolor, awaycolor):
    playNumber = np.array(playNumber)
    homeWinProbability = np.array(homeWinProbability)
    awayWinProbability = np.array(awayWinProbability)
    
    plt.figure()
    plt.ylabel("Win Probability (%)")
    plt.xlabel("")
    plt.title("Win Probability")
    plt.plot(playNumber, homeWinProbability, color = homecolor, label = hometeam)
    plt.plot(playNumber, awayWinProbability, color = awaycolor, label = awayteam)
    plt.ylim(-10, 110)
    plt.xticks([])
    plt.legend(loc="upper left")
    plt.savefig("outputWinProbability.png")
    plt.close()
    
# Iterate through the file and plot the score plot
def plotScorePlot(x, hometeam, awayteam, homeScore, awayScore, playNumber, homecolor, awaycolor, OTFlag):      
    playNumber = np.array(playNumber)
    homeScore = np.array(homeScore)
    awayScore = np.array(awayScore)

    plt.figure()
    plt.ylabel("Score")
    if(OTFlag == 1):
        plt.xlabel("Play Number")
        plt.title("Score Plot (OT)")
        plt.plot(playNumber, homeScore, color = homecolor, label = hometeam)
        plt.plot(playNumber, awayScore, color = awaycolor, label = awayteam)
    else:
        plt.xlabel("Time")
        plt.title("Score Plot")
        plt.plot(x, homeScore, color = homecolor, label = hometeam)
        plt.plot(x, awayScore, color = awaycolor, label = awayteam)
        plt.xticks(np.arange(0, 1681, 420), ['Q1', 'Q2', 'Q3', 'Q4', 'FINAL'])
        
    plt.legend(loc="upper left")
    plt.savefig("output.png")
    plt.close()
  
# Get the Vegas odds for the away team
def getAwayVegasOdds(homeelo, awayelo):
    constant = 18.14010981807
    odds = (float(homeelo) - float(awayelo))/constant
    return odds

# Get the Vegas odds for the home team    
def getHomeVegasOdds(homeelo, awayelo):
    constant = 18.14010981807
    odds = (float(awayelo) - float(homeelo))/constant
    return odds

# Get Elo Data
def getEloData():
    teamelocolumn = []
    elodatacolumn = []
    fbscolumn = fbsworksheet.col_values(2)
    fbscolumn.pop(0)
    fcscolumn = fcsworksheet.col_values(4)
    fcscolumn.pop(0)
    teamelocolumn.extend(fbscolumn)
    teamelocolumn.extend(fcscolumn)

    fbselocolumn = fbsworksheet.col_values(3)
    fbselocolumn.pop(0)
    fcselocolumn = fcsworksheet.col_values(1)
    fcselocolumn.pop(0)
    elodatacolumn.extend(fbselocolumn)
    elodatacolumn.extend(fcselocolumn)
    
    return {1: teamelocolumn, 2: elodatacolumn}
 
# Get color data
def getColorData():
    teamcolorcolumn = []
    colordatacolumn = []
    fbscolumn = colorworksheet.col_values(1)
    fbscolumn.pop(0)
    fcscolumn = colorworksheet.col_values(7)
    fcscolumn.pop(0)
    teamcolorcolumn.extend(fbscolumn)
    teamcolorcolumn.extend(fcscolumn)
    fbscolorcolumn = colorworksheet.col_values(4)
    fbscolorcolumn.pop(0)
    fcscolorcolumn = colorworksheet.col_values(10)
    fcscolorcolumn.pop(0)
    colordatacolumn.extend(fbscolorcolumn)
    colordatacolumn.extend(fcscolorcolumn)
    
    return {1: teamcolorcolumn, 2: colordatacolumn}
 
# Get the team hex color
def getColor(team, teamcolorcolumn, colordatacolumn):
    teamcolumn = teamcolorcolumn
    colorcolumn = colordatacolumn
    i = 0
    color = "black"
    for value in teamcolumn:
            if(team == value):
                color = colorcolumn[i]
                break
            i = i + 1  
    return color

# Get the team's elo
def getElo(team, teamelocolumn, elodatacolumn):
    teamcolumn = teamelocolumn
    elocolumn = elodatacolumn
    elo = 0
    i = 0
    for value in teamcolumn:
        if("(" in value):
            value = value.split("(")[0]
            value = value.strip()
        if(team == value):
            elo = elocolumn[i]
            break
        i = i + 1
    if(elo == 0):
        return -500
    return elo
        
# Convert seconds into minutes:seconds   
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%02d:%02d" % (minutes, seconds) 
   
# Parse the quarter
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
 
# Parse the current yard line
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
 
# Parse the current down and distance
def parseDown(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        # Get the time
        down = submissionbody.split("___")[4].split("\n")[4].split("|")[2]
    else:
        down = submissionbody.split("___")[3].split("\n")[4].split("|")[2]
    return down

# Parse who has the ball    
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
    
# Parse the time
def parseTime(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        # Get the time
        time = submissionbody.split("___")[4].split("\n")[4].split("|")[0]
    else:
        time = submissionbody.split("___")[4].split("\n")[3].split("|")[0]
    return time 
    
# Parse the home score
def parseHomeScore(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the home team's score
        homeTeamScore = scoreboard[4].split("**")[1]
    elif(len(submissionbody.split("___")) == 6):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the home team's score
        homeTeamScore = scoreboard[4].split("**")[1]
    elif(len(submissionbody.split("___")) == 5):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[4].split("\n")
        # Parse the home team's score
        homeTeamScore = scoreboard[4].split("**")[1]
    elif(len(submissionbody.split("___")) == 4):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[3].split("\n")
        # Parse the home team's score
        homeTeamScore = scoreboard[4].split("**")[1]
    elif(len(submissionbody.split("___")) == 3):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[2].split("\n")
        # Parse the home team's score
        homeTeamScore = scoreboard[3].split("**")[1]
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        # Parse the second team and their score
        homeTeamScore = scoreboard[2].split(" | ")[-1]
        
    return homeTeamScore

# Parse the away score
def parseAwayScore(submissionbody):
    if(len(submissionbody.split("___")) == 7):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the second team and their score
        awayTeamScore = scoreboard[5].split("**")[1]
    elif(len(submissionbody.split("___")) == 6):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the second team and their score
        awayTeamScore = scoreboard[5].split("**")[1]
    elif(len(submissionbody.split("___")) == 5):
        # Get the scoreboard portion of the submission'
        scoreboard = submissionbody.split("___")[4].split("\n")
        # Parse the second team and their score
        awayTeamScore = scoreboard[5].split("**")[1]
    elif(len(submissionbody.split("___")) == 4):
        # Get the scoreboard portion of the submission'
        scoreboard = submissionbody.split("___")[3].split("\n")
        # Parse the second team and their score
        awayTeamScore = scoreboard[5].split("**")[1]
    elif(len(submissionbody.split("___")) == 3):
        # Get the scoreboard portion of the submission'
        scoreboard = submissionbody.split("___")[2].split("\n")
        # Parse the second team and their score
        awayTeamScore = scoreboard[4].split("**")[1]
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        # Parse the second team and their score
        awayTeamScore = scoreboard[3].split(" | ")[-1]
    return awayTeamScore
    

# Parse the home team
def parseHomeTeam(submissionbody):
    homeTeam = "blank"
    print(len(submissionbody.split("___")))
    if(len(submissionbody.split("___")) == 7):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the first team and their score
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 6):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the first team and their score
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 5):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[4].split("\n")
        # Parse the first team and their score
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 4):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[3].split("\n")
        # Parse the first team and their score
        homeTeam = scoreboard[4].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 3):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[2].split("\n")
        # Parse the first team and their score
        homeTeam = scoreboard[3].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        # Parse the second team and their score
        homeTeam = scoreboard[2].split("]")[0]
        homeTeam = homeTeam.replace('[', '')
    return homeTeam

# Parse the away team
def parseAwayTeam(submissionbody):
    awayTeam = "blank"
    if(len(submissionbody.split("___")) == 7):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the second team and their score
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 6):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[5].split("\n")
        # Parse the second team and their score
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 5):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[4].split("\n")
        # Parse the second team and their score
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 4):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[3].split("\n")
        # Parse the second team and their score
        awayTeam = scoreboard[5].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 3):
        # Get the scoreboard portion of the submission
        scoreboard = submissionbody.split("___")[2].split("\n")
        # Parse the second team and their score
        awayTeam = scoreboard[4].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
    elif(len(submissionbody.split("___")) == 1):
        scoreboard = submissionbody.split("Q4")[1].split("\n")
        # Parse the second team and their score
        awayTeam = scoreboard[3].split("]")[0]
        awayTeam = awayTeam.replace('[', '')
    return awayTeam
      
# Iterate through Reddit to find the post game threads
def searchForGameThread(r, homeTeam, awayTeam, season, request, postseason):
    searchItem = "\"Game Thread\" \"" + homeTeam + "\" \"" + awayTeam + "\""
    print(searchItem)
    if(season == "s1"):
        season = "S1"
    if(season == "s2"):
        season = "S2"
    if(season == "s3"):
        season = "S3"
    if(season == "s4"):
        season = "S4"
    for submission in r.subreddit("FakeCollegeFootball").search(searchItem, sort='new'):
        # Get game thread submission day
        submissionTime = datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
        year = int(submissionTime.split("-")[0])
        month = int(submissionTime.split("-")[1])
        day = int(submissionTime.split("-")[2].split(" ")[0])
        homeTeam = homeTeam.lower()
        awayTeam = awayTeam.lower()
        if(request == "$score"):
            gameThread = searchForScoreGamethread(submission, homeTeam, awayTeam, season, request, postseason, day, month, year)
            if(gameThread != "NONE"):
                return gameThread
        elif(request == "$plot"):
            gameThread = searchForPlotGamethread(submission, homeTeam, awayTeam, season, request, postseason, day, month, year)
            if(gameThread != "NONE"):
                return gameThread
    return "NONE"
    
# Parse the URL from the post game thread
def parseURLFromGameThread(submissionbody, season):
    if("github" not in submissionbody and "pastebin" not in submissionbody):
        return "NO PLAYS"
    elif("Waiting on a response" in submissionbody):
        splitlist = submissionbody.split("Waiting on")[0].split("[Plays](")
        numItems = len(splitlist) - 1
        return splitlist[numItems].split(")")[0]
    else:
        splitlist = submissionbody.split("#Game complete")[0].split("[Plays](")
        numItems = len(splitlist) - 1
        return splitlist[numItems].split(")")[0]

# Seach for gamethread for the $plot command    
def searchForPlotGamethread(submission, homeTeam, awayTeam, season, request, postseason, day, month, year):
    away = "blank"
    home = "blank"
    if(submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Post Game Thread"
       or submission.link_flair_text == "Week 10 Game Thread"):
        away = parseAwayTeam(submission.selftext).lower()
        home = parseHomeTeam(submission.selftext).lower()
        if("–" in away):
            away = away.replace('–', '-')
        elif("–" in home):
            home = home.replace('–', '-')
        print(submission.title)
        print(submission.link_flair_text)
        print(away == homeTeam)
        print(away == awayTeam)
        print(home == homeTeam)
        print(home == awayTeam)
        print(away)
        print(home)
        print(awayTeam)
        print(homeTeam)
        print(day)
        print(month)
        print(year)
        print("\n")
    # If looking for season 4...
    if ((submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Week 10 Game Thread") and season == "S4" 
        and ((year == 2020 and month == 3 and day >= 20) or (year == 2020 and month > 3))
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        return submission
    # If looking for season 3...
    if ((submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Week 10 Game Thread") and season == "S3" 
        and ((year == 2020 and month <= 2 and day <= 15) or (year == 2020 and month < 2) or (year == 2019 and month == 7 and day >= 20) or (year == 2019 and month > 7)) 
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        if (postseason == 1 and (year == 2020 and month == 1 and day > 7) or (year == 2020 and month == 2 and day <= 16)):
            return submission
        elif (postseason == 0 and (year == 2020 and month == 1 and day <= 7) or (year == 2019)):
            return submission
    # If looking for season 2...
    if ((submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Week 10 Game Thread") and season == "S2" 
        and ((year == 2019 and month <= 6 and day <= 22) or (year == 2019 and month < 6) or (year == 2018 and month >= 11 and day >= 20) or (year == 2018 and month > 11)) 
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        if (postseason == 1 and (year == 2019 and month == 5 and day > 24) or (year == 2019 and month == 6 and day <= 23)):
            return submission
        elif (postseason == 0 and (year == 2019 and month <= 5 and day <= 24) or (year == 2018)):
            return submission
    # If looking for season 1...
    if (submission.link_flair_text == "Game Thread" and season == "S1" 
        and ((year == 2018 and month <= 11 and day <= 5) or (year == 2018 and month < 11) or (year == 2018 and month >= 1 and month < 11))
        and (homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away)):
        if (postseason == 1 and (year == 2018 and month == 9 and day > 20) or (year == 2018 and month == 10) or (year == 2018 and month == 11 and day <= 5)):
            return submission
        elif (postseason == 0 and (year == 2018 and month <= 9 and day <= 20) or (year == 2018 and month < 9)):
            return submission
    return "NONE"
    
# Seach for gamethread for the $score command
def searchForScoreGamethread(submission, homeTeam, awayTeam, season, request, postseason, day, month, year):
    away = "blank"
    home = "blank"
    if(submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Post Game Thread"
       or submission.link_flair_text == "Week 10 Game Thread"):
        away = parseAwayTeam(submission.selftext).lower()
        home = parseHomeTeam(submission.selftext).lower()
        print(submission.title)
        print(submission.link_flair_text)
        print(away)
        print(home)
        print(awayTeam)
        print(homeTeam)
        print(day)
        print(month)
        print(year)
        print("\n")
    # If looking for season 4...
    if ((submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Week 10 Game Thread") and season == "S4" 
        and ((year == 2020 and month == 3 and day >= 20) or (year == 2020 and month > 3))
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        return submission
    # If looking for season 3...
    if ((submission.link_flair_text == "Post Game Thread" or submission.link_flair_text == "Week 10 Game Thread") and season == "S3" 
        and ((year == 2020 and month <= 2 and day <= 15) or (year == 2020 and month < 2) or (year == 2019 and month == 7 and day >= 20) or (year == 2019 and month > 7)) 
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        if (postseason == 1 and (year == 2020 and month == 1 and day > 7) or (year == 2020 and month == 2 and day <= 16)):
            return submission
        elif (postseason == 0 and (year == 2020 and month == 1 and day <= 7) or (year == 2019)):
            return submission
    # If looking for season 2...
    if ((submission.link_flair_text == "Post Game Thread" or submission.link_flair_text == "Week 10 Game Thread") and season == "S2" 
        and ((year == 2019 and month <= 6 and day <= 22) or (year == 2019 and month < 6) or (year == 2018 and month >= 11 and day >= 20) or (year == 2018 and month > 11)) 
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        if (postseason == 1 and (year == 2019 and month == 5 and day > 24) or (year == 2019 and month == 6 and day <= 23)):
            return submission
        elif (postseason == 0 and (year == 2019 and month <= 5 and day <= 24) or (year == 2018)):
            return submission
    # If looking for season 1...
    if (submission.link_flair_text == "Post Game Thread" and season == "S1" 
        and ((year == 2018 and month <= 11 and day <= 5) or (year == 2018 and month < 11) or (year == 2018 and month >= 1 and month < 11))
        and (homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away)):
        if (postseason == 1 and (year == 2018 and month == 9 and day > 20) or (year == 2018 and month == 10) or (year == 2018 and month == 11 and day <= 5)):
            return submission
        elif (postseason == 0 and (year == 2018 and month <= 9 and day <= 20) or (year == 2018 and month < 9)):
            return submission
    return "NONE"
    
# Parse the data from the Pastebin play list
def parseDataFromPastebin(pastebinURL):
    #Parse data from the github url
    urlSplit = pastebinURL.split("/")
    url = "https://" + urlSplit[2] + "/raw/" + urlSplit[3]
    req = requests.get(url)

    data = ""
    for character in req.text:
        data = data + character
    return data

# Parse the data from the Github play list
def parseDataFromGithub(githubURL):
    #Parse data from the github url
    url = githubURL + "/raw"
    req = requests.get(url)
    
    #Remove the very first line from the data
    data = ""
    flag = 0
    for character in req.text:
        print(character)
        if(flag == 0 and character == "0"):
            data = data + "0"
            flag = 1
        elif(flag == 1 and character != "-"):
            data = data + character    
    return data

# Crawl through old season threads and plot the win probability and score
def threadCrawler(homeTeam, awayTeam, homeVegasOdds, awayVegasOdds, homeColor, awayColor, season, submission):
    submission.comment_sort = "old"

    if(homeTeam == "Massachusetts"):
        homeTeam = "UMass"
    elif(awayTeam == "Massachusetts"):
        awayTeam = "UMass"
    
    homeUser = ""
    awayUser = ""
    homeScore = 0
    awayScore = 0
    OTFlag = 0
    quarter = 1
    clock = "7:00"
    yardLine = 25
    possession = "home"
    down = 1
    distance = 10
    playType = "EMPTY"
    data = ""
    homeScoreList = []
    awayScoreList = []
    homeWinProbability = []
    awayWinProbability = []
    playNumber = []
    playCount = 1
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        if(OTFlag == 1):
            break
        if(comment.author == 'NFCAAOfficialRefBot' and 'you\'re home' in comment.body):
            homeUser = comment.body.split("The game has started!")[1].split(",")[0].strip()
            awayUser = comment.body.split("The game has started!")[1].split(",")[1].split("home. ")[1].strip()
        # Look through top level comment
        print(comment.author)
        if(comment.author == 'NFCAAOfficialRefBot' and 'has submitted their' in comment.body and OTFlag != 1):
            # Get the clock and quarter
            clock = comment.body.split("left in the")[0].split("on the")[-1].split(". ")[-1]
            quarter = comment.body.split("left in the ")[1].split(".")[0]
            if(quarter == "1st"):
                quarter = 1
            elif(quarter == "2nd"):
                quarter = 2
            elif(quarter == "3rd"):
                quarter = 3
            elif(quarter == "4th"):
                quarter = 4
            
            # Handle non kickoff and PATs
            if("kicking off" not in comment.body and "PAT" not in comment.body):
                # Get the down and distance
                down = comment.body.split("It\'s ")[-1].split(" and")[0]
                distance = comment.body.split("It\'s ")[-1].split(" and ")[1].split("on the")[0].strip()
                if(down == "1st"):
                    down = 1
                elif(down == "2nd"):
                    down = 2
                elif(down == "3rd"):
                    down = 3
                elif(down == "4th"):
                    down = 4
                    
                # Get the current possession
                possessionUser = comment.body.split(" reply ")[0].split("\n")[-1]
                if(possessionUser == homeUser):
                    possession = "home"
                elif(possessionUser == awayUser):
                    possession = "away"
                
                # Get the current yard line
                if("50" not in comment.body.split(" on the ")[1].split(".")[0].split(" ")):
                    yardLine = comment.body.split(" on the ")[1].split(".")[0].split(" ")[-1]
                    sideOfField = ""
                    for item in comment.body.split(" on the ")[1].split(".")[0].split(" ")[:-1]:
                        sideOfField = sideOfField + " " + item
                    sideOfField = sideOfField.strip()
                    if(possession == "home" and sideOfField == awayTeam):
                        yardLine = 100-int(yardLine)
                    elif(possession == "away" and sideOfField == homeTeam):
                        yardLine = 100-int(yardLine)
                else:
                    yardLine = 50
                
                # Handle "and goal" situations
                if(distance == "goal"):
                    distance = 100-int(yardLine)             
            else:
                down = 1
                distance = 10
            if("kicking off" in comment.body):
                yardLine = 35
                possessionUser = comment.body.split(" reply ")[0].split("\n")[-1]
                if(possessionUser == homeUser):
                    possession = "home"
                elif(possessionUser == awayUser):
                    possession = "away"
                
            if("PAT" in comment.body):
                yardLine = 97
                possessionUser = comment.body.split(" reply ")[0].split("\n")[-1]
                if(possessionUser == homeUser):
                    possession = "home"
                elif(possessionUser == awayUser):
                    possession = "away"
            for secondLevelComment in comment.replies:
                print(secondLevelComment.author)
                # Look through second level comment  
                if(" and " in homeUser):
                    homeUser1 = homeUser.split(" and ")[0]
                    homeUser2 = homeUser.split(" and ")[1]
                    print(homeUser1)
                    print(homeUser2)
                else:
                    homeUser1 = homeUser
                    homeUser2 = "BLANK USER"
                if(" and " in awayUser):
                    awayUser1 = awayUser.split(" and ")[0]
                    awayUser2 = awayUser.split(" and ")[1]
                else:
                    awayUser1 = awayUser
                    awayUser2 = "BLANK USER"
                if(secondLevelComment.author == homeUser1.split("/u/")[-1] or secondLevelComment.author == awayUser1.split("/u/")[-1]
                   or secondLevelComment.author == homeUser2.split("/u/")[-1] or secondLevelComment.author == awayUser2.split("/u/")[-1]):
                    commentList = secondLevelComment.body.split(" ")
                    if(OTFlag == 1):
                        break
                    commentList = [x.lower() for x in commentList]
                    if("normal" in commentList):
                        playType = "KICKOFF_NORMAL"
                    elif("squib" in commentList):
                        playType = "KICKOFF_SQUIB"
                    elif("onside" in commentList):
                        playType = "KICKOFF_ONSIDE"  
                    elif("pat" in commentList):
                        playType = "PAT"
                    elif("two" in commentList and "point" in commentList):
                        playType = "TWO_POINT"
                    else:
                        playType = "EMPTY"
                    for thirdLevelComment in secondLevelComment.replies:
                        if(season != "S1"):
                            #Look through third level comments
                            if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The two point was successful' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The two point was successful' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body 
                               and 'PAT or two point' not in thirdLevelComment.body and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 6
                                playType = "PAT"
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body
                               and 'PAT or two point' not in thirdLevelComment.body and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 6
                                playType = "PAT"
                        elif(season == "S1"):
                            #Look through third level comments
                            if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and homeTeam + " is kicking off"  in thirdLevelComment.body):
                                homeScore = homeScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The two point was successful' in thirdLevelComment.body
                               and homeTeam + " is kicking off" in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The two point was successful' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and homeTeam + " is kicking off" in thirdLevelComment.body):
                                homeScore = homeScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body 
                               and homeTeam + " just scored." in thirdLevelComment.body):
                                homeScore = homeScore + 6
                                playType = "PAT"
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body
                               and awayTeam + " just scored." in thirdLevelComment.body):
                                awayScore = awayScore + 6
                                playType = "PAT"
                        if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and  "we're going to overtime!" in thirdLevelComment.body):
                            OTFlag = 0
                            break
                        # Add data
                        if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and "I'm not waiting on a message from you" not in thirdLevelComment.body):
                            #Fill plot data
                            data = (data + str(homeScore) + " | " + str(awayScore) + " | " + str(quarter) + " | " + clock + " | " 
                                  + str(yardLine) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + playType + "\n")
                            homeScoreList.append(homeScore)
                            awayScoreList.append(awayScore)
                            playNumber.append(int(playCount))
                            playCount = playCount + 1
                            
                            m, s = clock.split(':')
                            time = int(m) * 60 + int(s)
                            
                            expectedPoints = calculateExpectedPoints(int(down), int(distance), int(yardLine), playType)  
                            if(possession == "home"):
                                curHomeWinProbability = calculateWinProbabilityOld(expectedPoints, int(quarter), time, homeScore, awayScore, int(down), int(distance), int(yardLine), playType, homeVegasOdds) * 100
                                curAwayWinProbability = 100 - curHomeWinProbability
                                homeWinProbability.append(curHomeWinProbability)
                                awayWinProbability.append(curAwayWinProbability)
                            elif(possession == "away"):
                                curAwayWinProbability = calculateWinProbabilityOld(expectedPoints, int(quarter), time, awayScore, homeScore, int(down), int(distance), int(yardLine), playType, awayVegasOdds) * 100
                                curHomeWinProbability = 100 - curAwayWinProbability
                                awayWinProbability.append(curAwayWinProbability)
                                homeWinProbability.append(curHomeWinProbability) 
                            
                        # If end of game, make sure WP is 100% and 0%
                        if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and "that's the end of the game" in thirdLevelComment.body):
                            homeScoreList.append(homeScore)
                            awayScoreList.append(awayScore)
                            playNumber.append(int(playCount))
                            playCount = playCount + 1
                            
                            m, s = clock.split(':')
                            time = 0.1
                            quarter = 4
                            
                            expectedPoints = calculateExpectedPoints(int(down), int(distance), int(yardLine), playType)  
                            if(possession == "home"):
                                curHomeWinProbability = calculateWinProbabilityOld(expectedPoints, int(quarter), time, homeScore, awayScore, int(down), int(distance), int(yardLine), playType, homeVegasOdds) * 100
                                curAwayWinProbability = 100 - curHomeWinProbability
                                homeWinProbability.append(curHomeWinProbability)
                                awayWinProbability.append(curAwayWinProbability)
                            elif(possession == "away"):
                                curAwayWinProbability = calculateWinProbabilityOld(expectedPoints, int(quarter), time, awayScore, homeScore, int(down), int(distance), int(yardLine), playType, awayVegasOdds) * 100
                                curHomeWinProbability = 100 - curAwayWinProbability
                                awayWinProbability.append(curAwayWinProbability)
                                homeWinProbability.append(curHomeWinProbability)
                            
    plotScorePlotOld(homeTeam, awayTeam, homeScoreList, awayScoreList, playNumber, homeColor, awayColor)
    plotWinProbabilityOld(homeTeam, awayTeam, homeWinProbability, awayWinProbability, playNumber, homeColor, awayColor)

# Calculate the current win probability                        
def calculateWinProbabilityOld(expectedPoints, quarter, time, teamScore, opponentScore, down, distance, yardLine, playType, vegasLine):    
    if(time == 0):
        time = 0.00001
    minutesInQuarter = time/60
    minutesRemaining = 28
    if(quarter == 1):
        minutesRemaining = 28-(7-minutesInQuarter)
    elif(quarter == 2):
        minutesRemaining = 21-(7-minutesInQuarter)
    elif(quarter == 3):
        minutesRemaining = 14-(7-minutesInQuarter)
    elif(quarter == 4):
        minutesRemaining = 7-(7-minutesInQuarter)
    else:
        minutesRemaining = 2
    
    if(minutesRemaining < 0):
        minutesRemaining = 0.01
        
    opponentMargin = opponentScore - teamScore
    opponentMargin = opponentMargin - expectedPoints
        
    stdDev = (13.45/math.sqrt((28/minutesRemaining)))
        
    winProbability = ((1-norm.cdf(((opponentMargin)+0.5),(-vegasLine*(minutesRemaining/28)),stdDev))
    +(0.5*(norm.cdf(((opponentMargin)+0.5), (-vegasLine*(minutesRemaining/28)), stdDev)
    - norm.cdf(((opponentMargin)-0.5),(-vegasLine*(minutesRemaining/28)), stdDev))))
    
    return winProbability
    
# Plot the win probability for the game
def plotWinProbabilityOld(hometeam, awayteam, homeWinProbability, awayWinProbability, playNumber, homecolor, awaycolor):
    playNumber = np.array(playNumber)
    homeWinProbability = np.array(homeWinProbability)
    awayWinProbability = np.array(awayWinProbability)
    
    plt.figure()
    plt.ylabel("Win Probability (%)")
    plt.xlabel("")
    plt.title("Win Probability")
    plt.plot(playNumber, homeWinProbability, color = homecolor, label = hometeam)
    plt.plot(playNumber, awayWinProbability, color = awaycolor, label = awayteam)
    plt.ylim(-10, 110)
    plt.xticks([])
    plt.legend(loc="upper left")
    plt.savefig("outputWinProbability.png")
    plt.close()
    
# Iterate through the file and plot the score plot
def plotScorePlotOld(hometeam, awayteam, homeScore, awayScore, playNumber, homecolor, awaycolor):      
    playNumber = np.array(playNumber)
    homeScore = np.array(homeScore)
    awayScore = np.array(awayScore)

    plt.ylabel("Score")
    plt.xlabel("")
    plt.title("Score Plot")
    plt.plot(playNumber, homeScore, color = homecolor, label = hometeam)
    plt.plot(playNumber, awayScore, color = awaycolor, label = awayteam)
    plt.xticks([])   
    plt.legend(loc="upper left")
    plt.savefig("output.png")
    plt.close()
          
# Main method
if __name__ == '__main__':
    r = loginReddit()
    loginDiscord(r)
    #print(calculateExpectedPoints(1, 10, 10, "PASS"))
    