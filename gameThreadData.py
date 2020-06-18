import praw
import requests
import datetime
from gameData import parseHomeTeam
from gameData import parseAwayTeam


"""
Gather the game thread information

@author: apkick
"""
    
"""
Search for a game thread based on what the user requests, searches for two teams in a time span range
based on what season the user wants to search. Season 4 is the default if they do not specify a season

"""
def searchForRequestGameThread(submission, homeTeam, awayTeam, season, request, postseason, day, month, year):
    if(request == "$score"):
        linkFlair = "Post Game Thread"
        linkFlair2 = "blank"
        linkFlair3 = "blank"
    elif(request == "$plot"):
        linkFlair = "Game Thread"
        linkFlair2 = "Week 10 Game Thread"
        linkFlair3 = "Week 9 Game Thread"
    away = "blank"
    home = "blank"
    if(submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Post Game Thread"
       or submission.link_flair_text == "Week 10 Game Thread" or submission.link_flair_text == "Week 9 Game Thread"
       or submission.link_flair_text == "Scrimmage"):
        away = parseAwayTeam(submission.selftext).lower()
        home = parseHomeTeam(submission.selftext).lower()
        print(submission.title)
        print(home)
        print(away)
        print(homeTeam)
        print(awayTeam)
        print(str(month) + " " + str(day) + " " + str(year))     
        print()
    # If looking for season 4...
    if ((submission.link_flair_text == "Game Thread" or submission.link_flair_text == "Week 10 Game Thread" or submission.link_flair_text == "Scrimmage") and season == "S4" 
        and ((year == 2020 and month == 3 and day >= 20) or (year == 2020 and month > 3)) and "MIAA" not in submission.title
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        return submission
    # If looking for season 3...
    if ((submission.link_flair_text == linkFlair or submission.link_flair_text == linkFlair2 or submission.link_flair_text == linkFlair3) and season == "S3" 
        and ((year == 2020 and month <= 2 and day <= 15) or (year == 2020 and month < 2) or (year == 2019 and month == 7 and day >= 20) or (year == 2019 and month > 7)) 
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        if (postseason == 1 and ((year == 2020 and month == 1 and day > 7) or (year == 2020 and month == 2 and day <= 16))):
            return submission
        elif (postseason == 0 and ((year == 2020 and month == 1 and day <= 7) or (year == 2019))):
            return submission
    # If looking for season 2...
    if ((submission.link_flair_text == linkFlair or submission.link_flair_text == linkFlair2 or submission.link_flair_text == linkFlair3) and season == "S2" 
        and ((year == 2019 and month <= 6 and day <= 22) or (year == 2019 and month < 6) or (year == 2018 and month >= 11 and day >= 20) or (year == 2018 and month > 11)) 
        and ((homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away))):
        if (postseason == 1 and ((year == 2019 and month == 5 and day > 24) or (year == 2019 and month == 6 and day <= 23))):
            return submission
        elif (postseason == 0 and ((year == 2019 and month <= 5 and day <= 24) or (year == 2019 and month < 5) or (year == 2018))):
            return submission
    # If looking for season 1...
    if ((submission.link_flair_text == linkFlair or submission.link_flair_text == linkFlair2 or submission.link_flair_text == linkFlair3) and season == "S1" 
        and ((year == 2018 and month <= 11 and day <= 5) or (year == 2018 and month < 11) or (year == 2018 and month >= 1 and month < 11))
        and (homeTeam == home or homeTeam == away) and (awayTeam == home or awayTeam == away)):
        if (postseason == 1 and ((year == 2018 and month == 9 and day > 20) or (year == 2018 and month == 10) or (year == 2018 and month == 11 and day <= 5))):
            return submission
        elif (postseason == 0 and ((year == 2018 and month <= 9 and day <= 20) or (year == 2018 and month < 9))):
            return submission
    return "NONE"

"""
Parse the data from the Github Gist into data.txt

"""
def parseDataFromGithub(githubURL):
    #Parse data from the github url
    url = githubURL + "/raw"
    req = requests.get(url)
    
    #Remove the very first line from the data
    data = ""
    flag = 0
    for character in req.text:
        if(flag == 0 and character == "0"):
            data = data + "0"
            flag = 1
        elif(flag == 1):
            data = data + character 
    if(data.find('--------------------------------------------------------------------------------\n') >= 0):
        data = data.replace('--------------------------------------------------------------------------------\n', '')
    return data

"""
Iterate through Reddit to find the game threads

"""
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
            gameThread = searchForRequestGameThread(submission, homeTeam, awayTeam, season, request, postseason, day, month, year)
            if(gameThread != "NONE"):
                print(gameThread.url)
                return gameThread
        elif(request == "$plot"):
            gameThread = searchForRequestGameThread(submission, homeTeam, awayTeam, season, request, postseason, day, month, year)
            if(gameThread != "NONE"):
                print(gameThread.url)
                return gameThread
    return "NONE"

"""
Iterate through Reddit to find the game thread and return a dictionary of the two teams in that game, with the 
1 value being the team you're looking for, 2 value being their opponent

"""
def searchForTeamGameThread(r, team):
    for submission in r.subreddit("FakeCollegeFootball").search(team, sort='new'):
        if(submission.link_flair_text == "Game Thread"):
            away = parseAwayTeam(submission.selftext)
            home = parseHomeTeam(submission.selftext)
        if (submission.link_flair_text == "Game Thread" and (team.lower() == home.lower() or team.lower() == away.lower())):
            if(team.lower() == home.lower()):
                return {1: home, 2: away}
            elif(team.lower() == away.lower()):
                return {1: away, 2: home}
    return {1: "NONE", 2: "NONE"}
    
"""
Parse the Gist url from the game thread

"""
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
    
"""
Save the Github Gist data into data.txt

"""
def saveGithubData(submissionbody, season):
    url = parseURLFromGameThread(submissionbody, season)
    if(url != "NO PLAYS"):
        data = parseDataFromGithub(url)
        text_file = open("data.txt", "w")
        text_file.write(data)
        text_file.close()
    return url
