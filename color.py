from sheets_functions import getColorData

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
        colorComparison = compareColor(homeColor, awayColor)
        if colorComparison[1] == colorComparison[2]:
            homeColor = "black"
            awayColor = "red"
        return {1: colorComparison[1], 2: colorComparison[2]}
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

def compareColor(homeColor, awayColor):
    homeHex = homeColor.split("#")[1]
    awayHex = awayColor.split("#")[1]
    homeDecimal = int(homeHex, 16) 
    awayDecimal = int(awayHex, 16)
    # If difference is greater than 330000 they are far enough apart
    if(abs(homeDecimal-awayDecimal) < 330000):
        homeColor = "black"
        awayColor = "red"
        return {1: homeColor, 2: awayColor}
    else:
        return {1: homeColor, 2: awayColor}
        
        