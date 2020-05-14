import csv
from winProbability import calculateExpectedPoints
from winProbability import calculateWinProbabilityGist
from plotGraphs import plotScorePlotGist
from plotGraphs import plotWinProbabilityGist

"""
Iterate through Gist data and post plots for that data

@author: apkick
"""

"""
Iterate through Gist data and post plots for that data for an ongoing game

"""
def iterateThroughGistDataOngoingGame(hometeam, awayteam, homeVegasOdds, awayVegasOdds, homecolor, awaycolor):
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
    rowCount = 1
    runoff = 0
    playTime = 0
    
    #Iterate through playlist file
    with open('data.txt', 'r+') as csvfile:
        counter = csv.reader(csvfile, delimiter= '|', lineterminator='\n')  
        rowCount = sum(1 for row in counter)
    with open('data.txt', 'r+') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n') 
        currentRow = 1
        for row in reader:
            if(len(row) > 2):
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
                if(quarter <= 4 and row[16] != "" and row[16] != "None"):
                    playTime = int(row[16])
                if(quarter <= 4 and row[17] != "" and row[17] != "None"):
                    runoff = int(row[17])
                    
                expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)   
                # Parse the win probability
                # Handle if points were scored
                if(row[5] == "home" and row[14] == "TOUCHDOWN"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "PAT")
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif(row[5] == "away" and row[14] == "TOUCHDOWN"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "PAT")
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                elif(row[5] == "home" and row[14] == "FIELD GOAL"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif(row[5] == "away" and row[14] == "FIELD GOAL"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                elif(row[5] == "home" and row[14] == "PAT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif(row[5] == "away" and row[14] == "PAT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                elif(row[5] == "home" and row[14] == "TWO POINT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif(row[5] == "away" and row[14] == "TWO POINT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                elif(row[5] == "home" and row[14] == "SAFETY"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif(row[5] == "away" and row[14] == "SAFETY"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                elif((row[5] == "home" and (row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT" and row[14] != "TOUCHBACK" and row[14] != "MISS")) 
                   or (row[5] == "away" and (row[14] == "KICK" or row[14] == "PUNT"))):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif((row[5] == "away" and (row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT" and row[14] != "TOUCHBACK" and row[14] != "MISS")) 
                   or (row[5] == "home" and (row[14] == "KICK" or row[14] == "PUNT"))):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                elif(row[5] == "away" and (row[14] == "TURNOVER" or row[14] == "MISS")):
                    yardLine = 100-yardLine
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif(row[5] == "home" and (row[14] == "TURNOVER" or row[14] == "MISS")):
                    yardLine = 100-yardLine
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                elif(row[5] == "away" and (row[14] == "TOUCHBACK")):
                    yardLine = 25
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(100-curHomeWinProbability)
                elif(row[5] == "home" and (row[14] == "TOUCHBACK")):
                    yardLine = 25
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(100-curAwayWinProbability)
                
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
            currentRow = currentRow + 1
    if(playTime is None):
        playTime = 0
    if(runoff is None):
        runoff = 0
    if(runoff is not None and playTime is not None and quarter is not None and time is not None and quarter == 4):
        if(rowCount == currentRow and (time-playTime-runoff) <= 0 and quarter == 4):        
            if(curHomeScore > curAwayScore):
                homeWinProbability.append(100)
                curHomeWinProbability = 100
                awayWinProbability.append(0)
                curAwayWinProbability = 0
                playNumber.append(int(playCount) + 1)
            elif(curHomeScore < curAwayScore):
                awayWinProbability.append(100)
                curAwayWinProbability = 100
                homeWinProbability.append(0)
                curHomeWinProbability = 0 
                playNumber.append(int(playCount) + 1)
    if(time <= 0 and quarter == 4):
        if(curHomeScore > curAwayScore):
            homeWinProbability.append(100)
            curHomeWinProbability = 100
            awayWinProbability.append(0)
            curAwayWinProbability = 0
            playNumber.append(int(playCount) + 1)
        elif(curHomeScore < curAwayScore):
            awayWinProbability.append(100)
            curAwayWinProbability = 100
            homeWinProbability.append(0)
            curHomeWinProbability = 0 
            playNumber.append(int(playCount) + 1)
        
    
    #Plot score plot
    plotScorePlotGist(xList, hometeam, awayteam, homeScore, awayScore, playNumber, homecolor, awaycolor, OTFlag)
   
    #Plot win probability
    plotWinProbabilityGist(hometeam, awayteam, homeWinProbability, awayWinProbability, playNumber, homecolor, awaycolor)


"""
Iterate through Gist data and post plots for a finished game

"""
def iterateThroughGistDataGameOver(hometeam, awayteam, homeVegasOdds, awayVegasOdds, homecolor, awaycolor):
    homeScore = []
    awayScore = []
    playNumber = []
    homeWinProbability = []
    awayWinProbability = []
    curHomeWinProbability = 0
    curAwayWinProbability = 0
    xList = []
    playCount = 1
    OTFlag = 0
    curHomeScore = 0
    curAwayScore = 0
    rowCount = 1
    runoff = 0
    playTime = 0
    
    #Iterate through playlist file
    with open('data.txt', 'r+') as csvfile:
        counter = csv.reader(csvfile, delimiter= '|', lineterminator='\n')  
        rowCount = sum(1 for row in counter)
    with open('data.txt', 'r+') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n') 
        currentRow = 1
        for row in reader:
            if(len(row) > 2):
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
                
                # Parse the win probability
                if(row[5] == "home"):
                    curHomeWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    curAwayWinProbability = 100 - curHomeWinProbability
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(curAwayWinProbability)
                if(row[5] == "away"):
                    curAwayWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
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
            currentRow = currentRow + 1
    if(curHomeScore > curAwayScore):
        homeWinProbability.append(100)
        curHomeWinProbability = 100
        awayWinProbability.append(0)
        curAwayWinProbability = 0
        playNumber.append(int(playCount) + 1)
    elif(curHomeScore < curAwayScore):
        awayWinProbability.append(100)
        curAwayWinProbability = 100
        homeWinProbability.append(0)
        curHomeWinProbability = 0 
        playNumber.append(int(playCount) + 1)
        
    
    #Plot score plot
    plotScorePlotGist(xList, hometeam, awayteam, homeScore, awayScore, playNumber, homecolor, awaycolor, OTFlag)
   
    #Plot win probability
    plotWinProbabilityGist(hometeam, awayteam, homeWinProbability, awayWinProbability, playNumber, homecolor, awaycolor)

