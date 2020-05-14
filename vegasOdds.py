from sheetsFunctions import getEloData

"""
Created on Wed May 13 19:58:18 2020

@author: apkick
"""

# Get the team's elo
def getElo(team, teamEloColumn, eloDataColumn):
    teamColumn = teamEloColumn
    eloColumn = eloDataColumn
    elo = 0
    i = 0
    for value in teamColumn:
        if("(" in value):
            value = value.split("(")[0]
            value = value.strip()
        if(team == value):
            elo = eloColumn[i]
            break
        i = i + 1
    if(elo == 0):
        return -500
    return elo

# Calculate the Vegas Odds
def calculateVegasOdds(teamElo, opponentElo):
    constant = 18.14010981807
    odds = (float(opponentElo) - float(teamElo))/constant
    return odds

# Return a dictionary containing the Vegas Odds for the game
def getVegasOdds(homeTeam, awayTeam):
    eloDictionary = getEloData()
    teamEloColumn = eloDictionary[1]
    eloDataColumn = eloDictionary[2]
    homeElo = getElo(homeTeam, teamEloColumn, eloDataColumn)
    awayElo = getElo(awayTeam, teamEloColumn, eloDataColumn)
    homeOdds = calculateVegasOdds(homeElo, awayElo)
    awayOdds = calculateVegasOdds(homeElo, awayElo)
    return{1: homeOdds, 2: awayOdds}
    
    

