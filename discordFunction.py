import praw
import discord
import datetime
from discord.ext import commands
from vegasOdds import getVegasOdds
from color import getTeamColors
from gameData import parseQuarter
from gameData import parseYardLine
from gameData import parseDown
from gameData import parsePossession
from gameData import parseTime
from gameData import parseHomeScore
from gameData import parseAwayScore
from gameData import parseHomeTeam
from gameData import parseAwayTeam
from gameThreadData import searchForGameThread
from gameThreadData import saveGithubData
from gistData import iterateThroughGistDataGameOver
from gistData import iterateThroughGistDataOngoingGame
from threadCrawler import threadCrawler
from winProbability import getCurrentWinProbability

"""
Handle the Discord side of the bot. Look for messages and post responses

@author: apkick
"""

"""
Fix naming inconsistencies between spreadsheets and Reddit Game Threads

"""
def handleNamingInconsistincies(team):
    if(team.find('amp;') >= 0):
        team = team.replace('amp;', '')
    if(team.find('–') >= 0):
        team = team.replace('–', '-')
    if(team == "UMass"):
        team = "Massachusetts"
    if(team == "Southern Mississippi"):
        team = "Southern Miss"
    if(team == "Miami (FL)"):
        team = "Miami"
    if(team == "Miami (OH)"):
        team = "Miami, OH"
    return team

"""
Change the user input team so that it can match for Reddit Game Threads

"""
def changeUserInputTeams(team):
    if(team.find('A&M') >= 0 or team.find('a&m') >= 0):
        team = team.replace('&', '&amp;')
    if(team == 'Miami' or team == 'miami'):
        team = 'miami (fl)'
    return team
 
"""
Parse what season the user is looking for, so that the bot knows which date 
range to look at. Also parse if the user is looking for a postseason game

"""
def parseSeason(awayTeam):
    postseason = 0
    season = "S4"
    if(("S1" in awayTeam or "S2" in awayTeam or "S3" in awayTeam or "S4" in awayTeam)
           or ("s1" in awayTeam or "s2" in awayTeam or "s3" in awayTeam or "s4" in awayTeam)):
        teamSplit = awayTeam.split(" ")
        i = 0
        for split in teamSplit:
            if(("S1" in split or "S2" in split or "S3" in split or "S4" in split)
               or ("s1" in split or "s2" in split or "s3" in split or "s4" in split)):
                season = teamSplit[i]
            if("postseason" in split or "Postseason" in split):
                postseason = 1
            i = i + 1
        awayTeam = awayTeam.split(season)[0] 
        awayTeam = awayTeam.strip()
    return {1: awayTeam, 2: season, 3: postseason}

"""
Make posts for ongoing games on Reddit

"""
async def makeOngoingGamePost(message, submission, curClock, curDown, curPossession, curYardLine, vegasOdds, team, opponentTeam, score, opponentScore, curWinProbability):
    odds = round(vegasOdds * 2) / 2
    if(odds == 0):
        odds = "Push"
    elif(odds > 0):
        odds = "+" + str(odds)
    post = "**" + curClock +  " | " + opponentTeam + " " + opponentScore + " " + team + " " + score + " (" + str(odds) + ")** \n"
    yardPost = curDown + " | :football: " + curPossession + " | " + curYardLine + "\n"
    winPost = "Each team has a 50% chance to win\n"
    if(int(curWinProbability) >= 50):
        winPost = team + " has a " + str(int(curWinProbability)) + "% chance to win\n"
    elif(int(curWinProbability) < 50):
        winPost = opponentTeam + " has a " + str(100-int(curWinProbability)) + "% chance to win\n"
    await message.channel.send(post + yardPost + winPost + submission.url + "\n")

"""
Get information to make a post for ongoing games on Reddit

"""
async def getOngoingGameInformation(message, submission, homeVegasOdds, awayVegasOdds, homeTeam, awayTeam, homeScore, awayScore):
    # Get win probability
    curPossession = parsePossession(submission.selftext)
    possessingTeamProbability = getCurrentWinProbability(homeVegasOdds, awayVegasOdds)
    if(curPossession == homeTeam):
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
    # If home team is winning or the score is tied
    if(int(homeScore) > int(awayScore) or int(homeScore) == int(awayScore)):
        await makeOngoingGamePost(message, submission, curClock, curDown, curPossession, curYardLine, homeVegasOdds, homeTeam, awayTeam, homeScore, awayScore, curHomeWinProbability)
    #If the home team is losing
    elif(int(homeScore) < int(awayScore)):
        await makeOngoingGamePost(message, submission, curClock, curDown, curPossession, curYardLine, awayVegasOdds, awayTeam, homeTeam, awayScore, homeScore, curAwayWinProbability)

"""
Make posts for games that went final on Reddit

"""
async def makeGameFinalScorePost(message, submission, team, opponentTeam, vegasOdds, score, opponentScore):
    odds = round(vegasOdds * 2) / 2
    numberOdds = odds
    if(odds == 0):
        odds = "Push"
    elif(odds > 0):
        odds = "+" + str(odds)
    post = "**FINAL | " + team + " defeated " + opponentTeam + " " + score + "-" + opponentScore + "**\n"
    if(int(numberOdds) > 0):
        await message.channel.send(post + "UPSET! " + team + " was underdogs at " + str(odds) + " and won!")
    if(int(numberOdds) < 0 and ((int(opponentScore) - int(score)) > numberOdds)):
        await message.channel.send(post + opponentTeam + " beat the spread listed at " + str(odds))
    elif(int(numberOdds) < 0 and ((int(opponentScore) - int(score)) < numberOdds)):
        print(numberOdds)
        await message.channel.send(post + team + " covered the spread listed at " + str(odds))
    if(int(numberOdds) == 0 or ((int(opponentScore) - int(score)) == numberOdds)):
        await message.channel.send(post + "This game was a push!")
        
"""
Handle everything that happens when a user commands $score, will post the current score of an
ongoing game or post a past game

"""
async def handleScoreMessage(r, message):
    if("vs" in message.content):
        if(message.content.startswith('$score')):
           teams = message.content.split("$score")[1]
        elif(message.content.startswith('$Score')):
            teams = message.content.split("$Score")[1]

        homeTeam = teams.split("vs")[0].strip()
        awayTeam = teams.split("vs")[1].strip()
        
        # Parse the season number from string
        parseSeasonDict = parseSeason(awayTeam)
        awayTeam = parseSeasonDict[1]
        season = parseSeasonDict[2]
        postseason = parseSeasonDict[3]
            
        lookingForThread = await message.channel.send("Looking for the game thread...")
        print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + homeTeam + " vs " + awayTeam)
        
        homeTeam = changeUserInputTeams(homeTeam)
        awayTeam = changeUserInputTeams(awayTeam)
        
        submission = searchForGameThread(r, homeTeam, awayTeam, season, "$score", postseason)
        if(submission == "NONE"):
            await message.channel.send("No game thread found.")
        else:
            print("GAME THREAD FOUND")
            
            url = saveGithubData(submission.selftext, season)
            homeTeam = parseHomeTeam(submission.selftext)
            awayTeam = parseAwayTeam(submission.selftext)
                        
            # Hardcode to fix inconsistencies in stat sheets
            homeTeam = handleNamingInconsistincies(homeTeam)
            awayTeam = handleNamingInconsistincies(awayTeam)
              
            # Get the vegas odds
            vegasOddsDict = getVegasOdds(homeTeam, awayTeam)
            homeVegasOdds = vegasOddsDict[1]
            awayVegasOdds = vegasOddsDict[2]
            
            # Get the score
            homeScore = parseHomeScore(submission.selftext)
            awayScore = parseAwayScore(submission.selftext)
                
            if("Game complete" in submission.selftext):
                if(season == "S4"):
                    if(int(homeScore) > int(awayScore) or int(homeScore) == int(awayScore)):
                        await makeGameFinalScorePost(message, submission, homeTeam, awayTeam, homeVegasOdds, homeScore, awayScore)
                    elif(int(homeScore) < int(awayScore)):
                        await makeGameFinalScorePost(message, submission, awayTeam, homeTeam, awayVegasOdds, awayScore, homeScore)  
                else:
                    post = "blank"
                    if(int(homeScore) > int(awayScore)):
                        post = "**FINAL | " + homeTeam + " defeated " + awayTeam + " " + homeScore + "-" + awayScore + "**\n"
                    else:
                        post = "**FINAL | " + awayTeam + " defeated " + homeTeam + " " + awayScore + "-" + homeScore + "**\n"
                    await message.channel.send(post)
            else:
                if(season == "S4"):
                    await getOngoingGameInformation(message, submission, homeVegasOdds, awayVegasOdds, homeTeam, awayTeam, homeScore, awayScore)
                
                else:
                    post = "blank"
                    if(int(homeScore) > int(awayScore)):
                        post = "**FINAL | " + homeTeam + " defeated " + awayTeam + " " + homeScore + "-" + awayScore + "**\n"
                    else:
                        post = "**FINAL | " + awayTeam + " defeated " + homeTeam + " " + awayScore + "-" + homeScore + "**\n"
                    await message.channel.send(post)      
        await message.channel.delete(lookingForThread)
    else: 
        await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")
        
"""
Handle everything that happens when a user commands $plot, will post the current plot of an
ongoing game or post a past game

"""    
async def handlePlotMessage(r, message):
    if("vs" in message.content):
        if(message.content.startswith('$plot')):
           teams = message.content.split("$plot")[1]
        elif(message.content.startswith('$Plot')):
            teams = message.content.split("$Plot")[1]

        homeTeam = teams.split("vs")[0].strip()
        awayTeam = teams.split("vs")[1].strip()
        
        # Parse the season number from string
        parseSeasonDict = parseSeason(awayTeam)
        awayTeam = parseSeasonDict[1]
        season = parseSeasonDict[2]
        postseason = parseSeasonDict[3]
        
        lookingForThread = await message.channel.send("Looking for the game thread...")
        print("LOOKING FOR THREAD WITH THE FOLLOWING MATCHUP: " + homeTeam + " vs " + awayTeam)
        
        homeTeam = changeUserInputTeams(homeTeam)
        awayTeam = changeUserInputTeams(awayTeam)
        
        # Look for game thread
        submission = searchForGameThread(r, homeTeam, awayTeam, season, "$plot", postseason)
        if(submission == "NONE"):
            await message.channel.send("No game thread found.")
        else:
            print("GAME THREAD FOUND")
            
            # Parse data from url
            url = saveGithubData(submission.selftext, season)
            homeTeam = parseHomeTeam(submission.selftext)
            awayTeam = parseAwayTeam(submission.selftext)
                        
            # Hardcode to fix inconsistencies in stat sheets
            homeTeam = handleNamingInconsistincies(homeTeam)
            awayTeam = handleNamingInconsistincies(awayTeam)
             
            #Get team colors for plots
            colorDict = getTeamColors(homeTeam, awayTeam)
            homeColor = colorDict[1]
            awayColor = colorDict[2]
              
            # Get the vegas odds
            vegasOddsDict = getVegasOdds(homeTeam, awayTeam)
            homeVegasOdds = vegasOddsDict[1]
            awayVegasOdds = vegasOddsDict[2]

            #Work with new gist
            if(season == "S4"):
                if("Game complete" in submission.selftext):
                    #If there is a GitHub URL as plays have been called
                    if(url != "NO PLAYS"):
                        # Iterate through the data and plot the graphs
                        iterateThroughGistDataOngoingGame(homeTeam, awayTeam, homeVegasOdds, awayVegasOdds, homeColor, awayColor)
                        
                        # Send score plot
                        with open('output.png', 'rb') as fp:
                            await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                            
                        # Send the win probability plot
                        with open('outputWinProbability.png', 'rb') as fp:
                            await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                    else:
                        await message.channel.send("No plays for the game found.")
                else:
                    #If there is a GitHub URL as plays have been called
                    if(url != "NO PLAYS"):
                        # Iterate through the data and plot the graphs
                        iterateThroughGistDataOngoingGame(homeTeam, awayTeam, homeVegasOdds, awayVegasOdds, homeColor, awayColor)
                        
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
                submissionTime = datetime.datetime.fromtimestamp(int(submission.created_utc)).strftime('%Y-%m-%d %H:%M:%S')
                year = int(submissionTime.split("-")[0])
                month = int(submissionTime.split("-")[1])
                day = int(submissionTime.split("-")[2].split(" ")[0])
                if(year > 2018 or (year == 2018 and month == 8 and day > 25) or (year == 2018 and month > 8)):
                    oldThread = await message.channel.send("Iterating through old thread to generate plots...")
                    threadCrawler(homeTeam, awayTeam, homeVegasOdds, awayVegasOdds, homeColor, awayColor, season, submission)
                    # Send score plot
                    with open('output.png', 'rb') as fp:
                        await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                            
                    # Send the win probability plot
                    with open('outputWinProbability.png', 'rb') as fp:
                        await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                    await message.channel.delete(oldThread)
                else:
                    await message.channel.send("This game is too old to plot the data. I can only plot Season I, Week 11 games onward")
        await message.channel.delete(lookingForThread)
    else: 
        await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")

"""
Login to Discord and run the bot

"""
def loginDiscord(r):
    token = 'NzA4ODIzNzc3NDI0NzAzNTE5.Xrc9tA.vcsJTLYrVqomAFSnLwY09BlXzYE'

    client = discord.Client()

    @client.event
    async def on_message(message):
        global postEdited, changeIndex
        
        if(message.content.startswith('$score') or message.content.startswith('$Score')):
           await handleScoreMessage(r, message)
        
        elif(message.content.startswith('$plot') or message.content.startswith('$Plot')):
            await handlePlotMessage(r, message)
                
    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token) 