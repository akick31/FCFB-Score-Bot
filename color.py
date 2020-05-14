from sheetsFunctions import getColorData

"""
Created on Wed May 13 20:15:46 2020

@author: apkick
"""

def getTeamColors(homeTeam, awayTeam):
    colorDict = getColorData()
    teamColorColumn = colorDict[1]
    colorDataColumn = colorDict[2]
    homeColor = getColor(homeTeam, teamColorColumn, colorDataColumn)
    awayColor = getColor(awayTeam, teamColorColumn, colorDataColumn)
    return {1: homeColor, 2: awayColor}
    
def getColor(team, teamColorColumn, colorDataColumn):
    teamColumn = teamColorColumn
    colorColumn = colorDataColumn
    i = 0
    color = "black"
    for value in teamColumn:
            if(team == value):
                color = colorColumn[i]
                break
            i = i + 1  
    return color

