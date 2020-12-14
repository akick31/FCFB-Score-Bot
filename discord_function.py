import praw
import discord
import datetime
from discord.ext import commands
from name_fix import handleNamingInconsistincies
from name_fix import changeUserInputTeams
from vegas_odds import getVegasOdds
from color import getTeamColors
from game_data import parseQuarter
from game_data import parseYardLine
from game_data import parseDown
from game_data import parsePossession
from game_data import parseTime
from game_data import parseHomeScore
from game_data import parseAwayScore
from game_data import parseHomeTeam
from game_data import parseAwayTeam
from game_data import parseHomeUser
from game_data import parseAwayUser
from game_data import parseWaitingOn
from game_thread_data import searchForGameThread
from game_thread_data import searchForTeamGameThread
from game_thread_data import saveGithubData
from gist_data import iterateThroughGistDataGameOver
from gist_data import iterateThroughGistDataOngoingGame
from thread_crawler import threadCrawler
from win_probability import getCurrentWinProbability
from sheets_functions import getStandingsData
from sheets_functions import getRankingsData

"""
Handle the Discord side of the bot. Look for messages and post responses

@author: apkick
"""
 
"""
Parse what season the user is looking for, so that the bot knows which date 
range to look at. Also parse if the user is looking for a postseason game

"""
def parseSeason(awayTeam):
    postseason = 0
    season = "S5"
    if(("S1" in awayTeam or "S2" in awayTeam or "S3" in awayTeam or "S4" in awayTeam or "S5" in awayTeam)
           or ("s1" in awayTeam or "s2" in awayTeam or "s3" in awayTeam or "s4" in awayTeam or "s5" in awayTeam)):
        teamSplit = awayTeam.split(" ")
        i = 0
        for split in teamSplit:
            if(("S1" in split or "S2" in split or "S3" in split or "S4" in split or "S5" in split)
               or ("s1" in split or "s2" in split or "s3" in split or "s4" in split or "s5" in split)):
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
async def makeOngoingGamePost(message, submission, curClock, curDown, curPossession, curYardLine, vegasOdds, team, opponentTeam, score, opponentScore, curwin_probability, waitingOn):
    odds = round(vegasOdds * 2) / 2
    if(odds == 0):
        odds = "Push"
    elif(odds > 0):
        odds = "+" + str(odds)
    post = "**" + curClock +  " | " + opponentTeam + " " + opponentScore + " " + team + " " + score + " (" + str(odds) + ")** \n"
    yardPost = curDown + " | :football: " + curPossession + " | " + curYardLine + "\n"
    winPost = "Each team has a 50% chance to win\n"
    if(int(curwin_probability) >= 50):
        winPost = team + " has a " + str(int(curwin_probability)) + "% chance to win\n"
    elif(int(curwin_probability) < 50):
        winPost = opponentTeam + " has a " + str(100-int(curwin_probability)) + "% chance to win\n"
    waitingOnPost = "Waiting on " + waitingOn + " for a number\n"
    await message.channel.send(post + yardPost + winPost + waitingOnPost + submission.url + "\n")

"""
Get information to make a post for ongoing games on Reddit

"""
async def getOngoingGameInformation(message, submission, homeVegasOdds, awayVegasOdds, homeTeam, awayTeam, homeScore, awayScore):
    # Get win probability
    curPossession = parsePossession(submission.selftext)
    possessingTeamProbability = getCurrentWinProbability(homeVegasOdds, awayVegasOdds)
    if(curPossession == homeTeam):
        curHomewin_probability = possessingTeamProbability
    else:
        curHomewin_probability = 100-possessingTeamProbability
    curAwaywin_probability = 100-curHomewin_probability
    # Get other game data
    curYardLine = parseYardLine(submission.selftext)
    curQuarter = parseQuarter(submission.selftext)
    curDown = parseDown(submission.selftext)
    curTime = parseTime(submission.selftext)
    homeUser = parseHomeUser(submission.selftext)
    awayUser = parseAwayUser(submission.selftext)
    waitingOn = parseWaitingOn(submission.selftext, homeUser, awayUser, homeTeam, awayTeam)
    # If game is final, display that
    if(curQuarter == "OT"):
        curClock = "OT"
    else:
        curClock = str(curTime) + " " + str(curQuarter) 
    # If home team is winning or the score is tied
    if(int(homeScore) > int(awayScore) or int(homeScore) == int(awayScore)):
        await makeOngoingGamePost(message, submission, curClock, curDown, curPossession, curYardLine, homeVegasOdds, homeTeam, awayTeam, homeScore, awayScore, curHomewin_probability, waitingOn)
    #If the home team is losing
    elif(int(homeScore) < int(awayScore)):
        await makeOngoingGamePost(message, submission, curClock, curDown, curPossession, curYardLine, awayVegasOdds, awayTeam, homeTeam, awayScore, homeScore, curAwaywin_probability, waitingOn)

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
            if vegasOddsDict != "There was an error in contacting Google Sheets, please try again.":
                homeVegasOdds = vegasOddsDict[1]
                awayVegasOdds = vegasOddsDict[2]
                # Get the score
                homeScore = parseHomeScore(submission.selftext)
                awayScore = parseAwayScore(submission.selftext)
                    
                if("Game complete" in submission.selftext):
                    if(season == "S5"):
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
                    if(season == "S5"):
                        await getOngoingGameInformation(message, submission, homeVegasOdds, awayVegasOdds, homeTeam, awayTeam, homeScore, awayScore)
                    
                    else:
                        post = "blank"
                        if(int(homeScore) > int(awayScore)):
                            post = "**FINAL | " + homeTeam + " defeated " + awayTeam + " " + homeScore + "-" + awayScore + "**\n"
                        else:
                            post = "**FINAL | " + awayTeam + " defeated " + homeTeam + " " + awayScore + "-" + homeScore + "**\n"
                        await message.channel.send(post) 
            else:
                await message.channel.send("There was an error in contacting Google Sheets, please try again.")
            
                 
        await lookingForThread.delete()
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
            if colorDict != "There was an error in contacting Google Sheets, please try again.":
                homeColor = colorDict[1]
                awayColor = colorDict[2]
                vegasOddsDict = getVegasOdds(homeTeam, awayTeam)
                # Get the vegas odds
                if vegasOddsDict != "There was an error in contacting Google Sheets, please try again.":
                    homeVegasOdds = vegasOddsDict[1]
                    awayVegasOdds = vegasOddsDict[2]
                    #Work with new gist
                    if(season == "S5" or season == "S4"):
                        if("Game complete" in submission.selftext):
                            #If there is a GitHub URL as plays have been called
                            if(url != "NO PLAYS"):
                                # Iterate through the data and plot the graphs
                                iterateThroughGistDataGameOver(homeTeam, awayTeam, homeVegasOdds, awayVegasOdds, homeColor, awayColor)
                                
                                # Send score plot
                                with open('output.png', 'rb') as fp:
                                    await message.channel.send(file=discord.File(fp, 'new_filename.png'))
                                    
                                # Send the win probability plot
                                with open('outputwin_probability.png', 'rb') as fp:
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
                                with open('outputwin_probability.png', 'rb') as fp:
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
                            with open('outputwin_probability.png', 'rb') as fp:
                                await message.channel.send(file=discord.File(fp, 'new_win_probability.png'))
                            await oldThread.delete()
                        else:
                            await message.channel.send("This game is too old to plot the data. I can only plot Season I, Week 11 games onward")
                else:
                    await message.channel.send("There was an error in contacting Google Sheets, please try again.")
            else:
                await message.channel.send("There was an error in contacting Google Sheets, please try again.")

            
        await lookingForThread.delete()
    else: 
        await message.channel.send("Incorrect format. Format needs to be [team] vs [team]")

"""
Handle when the user requests the conference standings

"""
async def handleStandingsMessage(r, message):
    if(message.content.startswith('$standings')):
        conference = message.content.split("$standings")[1].strip()
    elif(message.content.startswith('$Standings')):
        conference = message.content.split("$Standings")[1].strip()
    elif(message.content.startswith('$standing')):
        conference = message.content.split("$standing")[1].strip()
    elif(message.content.startswith('$Standing')):
        conference = message.content.split("$Standing")[1].strip()
    post = getStandingsData(conference)
    await message.channel.send(post)
    
"""
Handle when the user requests a ranking

"""    
async def handleRankingsMessage(r, message):
    if(message.content.startswith('$rankings')):
        request = message.content.split("$rankings")[1].strip()
    elif(message.content.startswith('$Rankings')):
        request = message.content.split("$Rankings")[1].strip()
    if(request == "" or request == " "):
        await message.channel.send("The $rankings command currently supports the following ranks commands:\n" +
                                   "- FBS Coaches Poll\n- FCS Coaches Poll\n- FBS Elo\n- FCS Elo\n- MOV (FBS Only)\n- Scoring Offense (FBS Only)\n- Scoring Defense (FBS Only)\n" + 
                                   "- SOSMOV (FBS Only)\n- EQW (FBS Only)\n- Composite (FBS Only)\n- Adjusted Strength Rating (FBS Only)\n- Colley Matrix (FBS Only)\n" + 
                                   "- Adjusted Speed (FBS Only)\n" + "- Raw Speed (FBS Only)\n" + "**If you want a ranking added, please contact Dick**")
    else:
        post = getRankingsData(r, request)
        await message.channel.send(post)

"""
Handle when the user requests a team's opponent

"""   
async def handleOpponentMessage(r, message):
    if(message.content.startswith('$opponent')):
        team = message.content.split("$opponent")[1].strip()
    elif(message.content.startswith('$Opponent')):
        team = message.content.split("$Opponent")[1].strip()

    lookingForThread = await message.channel.send("Looking for the most recent game thread with the following team: " + team)
    print("LOOKING FOR THREAD WITH THE FOLLOWING TEAM: " + team)
    
    team = changeUserInputTeams(team)
    
    opponent = searchForTeamGameThread(r, team) 
    # opponent[1] is team, opponent[2] is the opponent
    if(opponent[1] == "NONE"):
        await message.channel.send("No game thread found.")
    else:
        await message.channel.send(opponent[1] + " is playing " + opponent[2])
    await lookingForThread.delete()

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
            
        elif(message.content.startswith('$Standings') or message.content.startswith('$standings') or 
             message.content.startswith('$Standing') or message.content.startswith('$standing')):
            await handleStandingsMessage(r, message)
            
        elif(message.content.startswith('$Rankings') or message.content.startswith('$rankings')):
            await handleRankingsMessage(r, message)

        elif(message.content.startswith('$Opponent') or message.content.startswith('$opponent')):
            await handleOpponentMessage(r, message)
                
    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(token) 