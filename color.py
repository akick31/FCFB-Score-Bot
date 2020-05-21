from sheetsFunctions import getColorData

"""
Handle the colors aspect of the bot

@author: apkick
"""

"""
Get the colors for both teams playing

"""
def getTeamColors(homeTeam, awayTeam):
    colorDict = getColorData()
    if colorDict != "There was an error in contacting Google Sheets, please try again.":
        teamColorColumn = colorDict[1]
        colorDataColumn = colorDict[2]
        homeColor = getColor(homeTeam, teamColorColumn, colorDataColumn)
        awayColor = getColor(awayTeam, teamColorColumn, colorDataColumn)
        return {1: homeColor, 2: awayColor}
    else:
        return "There was an error in contacting Google Sheets, please try again."

"""
Return the color for the team requested

"""    
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

