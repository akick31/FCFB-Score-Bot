import math
import csv
from scipy.stats import norm

"""
Calculate the win probability for various scenarios

@author: apkick
"""

"""
Get the current win probability for the current play for an ongoing game

"""
def getCurrentWinProbability(homeVegasOdds, awayVegasOdds):
    winProbability = []
    
    #Iterate through playlist file
    with open('data.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n')
        for row in reader:
            if(len(row) > 2):
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
                if((row[5] == "home" and row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT" and row[14] != "TOUCHBACK" and row[14] != "MISS")
                   or (row[5] == "away" and (row[14] == "KICK" or row[14] == "PUNT" or row[14] == "TOUCHBACK"))):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                elif((row[5] == "away" and row[14] != "TURNOVER" and row[14] != "KICK" and row[14] != "PUNT" and row[14] != "TOUCHBACK" and row[14] != "MISS") 
                   or (row[5] == "home" and (row[14] == "KICK" or row[14] == "PUNT"))):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                elif(row[5] == "away" and (row[14] == "TURNOVER" or row[14] == "MISS")):
                    yardLine = 100-yardLine
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                elif(row[5] == "home" and (row[14] == "TURNOVER" or row[14] == "MISS")):
                    yardLine = 100-yardLine
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                elif(row[5] == "away" and (row[14] == "TOUCHBACK")):
                    yardLine = 25
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                elif(row[5] == "home" and (row[14] == "TOUCHBACK")):
                    yardLine = 25
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, playType)
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                # Handle if points were scored
                if(row[5] == "home" and row[14] == "TOUCHDOWN"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "PAT")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]) + 6, int(row[1]), down, distance, yardLine, "PAT", homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "TOUCHDOWN"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "PAT")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]) + 6, int(row[0]), down, distance, yardLine, "PAT", awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "FIELD GOAL"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]) + 3, int(row[1]), down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "FIELD GOAL"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]) + 3, int(row[0]), down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "PAT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]) + 1, int(row[1]), down, distance, yardLine, "KICKOFF", homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "PAT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]) + 1, int(row[0]), down, distance, yardLine, "KICKOFF", awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "TWO POINT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]) + 2, int(row[1]), down, distance, yardLine, "KICKOFF", homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "TWO POINT"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]) + 2, int(row[0]), down, distance, yardLine, "KICKOFF", awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "home" and row[14] == "SAFETY"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[0]), int(row[1]) + 2, down, distance, yardLine, playType, homeVegasOdds) * 100
                    winProbability.append(curWinProbability)
                if(row[5] == "away" and row[14] == "SAFETY"):
                    expectedPoints = calculateExpectedPoints(down, distance, yardLine, "KICKOFF")
                    curWinProbability = calculateWinProbabilityGist(expectedPoints, quarter, time, int(row[1]), int(row[0]) + 2, down, distance, yardLine, playType, awayVegasOdds) * 100
                    winProbability.append(curWinProbability)
                    
        return winProbability[-1]
    
"""
Calculate the win probability for the thread crawler

"""                     
def calculateWinProbabilityThreadCrawler(expectedPoints, quarter, time, teamScore, opponentScore, down, distance, yardLine, playType, vegasLine):    
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

"""
Calculate the win probability for the Gist data

""" 
def calculateWinProbabilityGist(expectedPoints, quarter, time, teamScore, opponentScore, down, distance, yardLine, playType, vegasLine):  
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
    
"""
Calculate the expected points, used to tell the formula information so it can calculate
based on current scenarios

""" 
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
