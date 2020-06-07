import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pollData import getCoachesPollData

"""
Handle contacting Google Sheets and getting information from the document

@author: apkick
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

sh4 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1m-_pHJK-40lc9v8tZf7IFIv3Ac7R2UTywMvvmQibsQI/edit?usp=sharing')
standingsworksheet = sh4.worksheet("Standings")
rankingsworksheet = sh4.worksheet("Rankings")
compositeworksheet = sh4.worksheet("Composite")

sh5 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1IrBBMKApJVYlU10wCOKp_oW3wvQfFT-xTC_A6EHJlzU/edit?usp=sharing')
fcsstandingsworksheet = sh5.worksheet("Sheet1")

sh6 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1GDDwQ2FpZIgGoDdZoRNbBg8IyQir2-WZriz8bHHXbSE/edit?usp=sharing')
sosmovrworksheet = sh6.worksheet("SOSMOVR")

sh7 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1QWakYxpH0bV0dJGgZ11kmOqsUxbD1GYlJd22TKUaP0k/edit?usp=sharing')
speedworksheet = sh7.worksheet("Quickest Team Ranking")

"""
Get Elo data from both FBS and FCS sheets

"""
def getEloData():
    try:
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
    except:
        return "There was an error in contacting Google Sheets, please try again."
 
"""
Get Hex Color data for both FBS and FCS teams

"""
def getColorData():
    try:
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
    except:
        return "There was an error in contacting Google Sheets, please try again."

"""
Get the ACC standings from CHEFF

"""
def parseACC():
    post = "----------------------\n**ACC**\n----------------------\n----------------------\nAtlantic\n----------------------\n"
    teamColumn = standingsworksheet.col_values(2)
    teamConferenceColumn = standingsworksheet.col_values(3)
    teamOverallColumn = standingsworksheet.col_values(4)
    for i in range (6, 13):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nCoastal\n----------------------\n"
    teamColumn = standingsworksheet.col_values(5)
    teamConferenceColumn = standingsworksheet.col_values(6)
    teamOverallColumn = standingsworksheet.col_values(7)
    for i in range (6, 13):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the AAC standings from CHEFF

"""
def parseAAC():
    post = "----------------------\n**American**\n----------------------\n----------------------\nEast\n----------------------\n"
    teamColumn = standingsworksheet.col_values(9)
    teamConferenceColumn = standingsworksheet.col_values(10)
    teamOverallColumn = standingsworksheet.col_values(11)
    for i in range (6, 12):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    teamColumn = standingsworksheet.col_values(12)
    teamConferenceColumn = standingsworksheet.col_values(13)
    teamOverallColumn = standingsworksheet.col_values(14)
    for i in range (6, 12):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Big 10 standings from CHEFF

"""
def parseBigTen():
    post = "----------------------\n**Big Ten**\n----------------------\n----------------------\nEast\n----------------------\n"
    teamColumn = standingsworksheet.col_values(16)
    teamConferenceColumn = standingsworksheet.col_values(17)
    teamOverallColumn = standingsworksheet.col_values(18)
    for i in range (6, 13):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    teamColumn = standingsworksheet.col_values(19)
    teamConferenceColumn = standingsworksheet.col_values(20)
    teamOverallColumn = standingsworksheet.col_values(21)
    for i in range (6, 13):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Pac 12 standings from CHEFF

"""
def parsePac12():
    post = "----------------------\n**Pac-12**\n----------------------\n----------------------\nNorth\n----------------------\n"
    teamColumn = standingsworksheet.col_values(2)
    teamConferenceColumn = standingsworksheet.col_values(3)
    teamOverallColumn = standingsworksheet.col_values(4)
    for i in range (28, 34):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nSouth\n----------------------\n"
    teamColumn = standingsworksheet.col_values(5)
    teamConferenceColumn = standingsworksheet.col_values(6)
    teamOverallColumn = standingsworksheet.col_values(7)
    for i in range (28, 34):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the CUSA standings from CHEFF

"""
def parseCUSA():
    post = "----------------------\n**Conference USA**\n----------------------\n----------------------\nEast\n----------------------\n"
    teamColumn = standingsworksheet.col_values(2)
    teamConferenceColumn = standingsworksheet.col_values(3)
    teamOverallColumn = standingsworksheet.col_values(4)
    for i in range (17, 24):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    teamColumn = standingsworksheet.col_values(5)
    teamConferenceColumn = standingsworksheet.col_values(6)
    teamOverallColumn = standingsworksheet.col_values(7)
    for i in range (17, 24):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the MAC standings from CHEFF

"""
def parseMAC():
    post = "----------------------\n**MAC**\n----------------------\n----------------------\nEast\n----------------------\n"
    teamColumn = standingsworksheet.col_values(9)
    teamConferenceColumn = standingsworksheet.col_values(10)
    teamOverallColumn = standingsworksheet.col_values(11)
    for i in range (17, 23):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    teamColumn = standingsworksheet.col_values(12)
    teamConferenceColumn = standingsworksheet.col_values(13)
    teamOverallColumn = standingsworksheet.col_values(14)
    for i in range (17, 23):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Mountain West standings from CHEFF

"""
def parseMWC():
    post = "----------------------\n**Mountain West**\n----------------------\n----------------------\nMountain\n----------------------\n"
    teamColumn = standingsworksheet.col_values(16)
    teamConferenceColumn = standingsworksheet.col_values(17)
    teamOverallColumn = standingsworksheet.col_values(18)
    for i in range (17, 23):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    teamColumn = standingsworksheet.col_values(19)
    teamConferenceColumn = standingsworksheet.col_values(20)
    teamOverallColumn = standingsworksheet.col_values(21)
    for i in range (17, 23):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the SEC standings from CHEFF

"""
def parseSEC():
    post = "----------------------\n**SEC**\n----------------------\n----------------------\nEast\n----------------------\n"
    teamColumn = standingsworksheet.col_values(9)
    teamConferenceColumn = standingsworksheet.col_values(10)
    teamOverallColumn = standingsworksheet.col_values(11)
    for i in range (28, 35):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    teamColumn = standingsworksheet.col_values(12)
    teamConferenceColumn = standingsworksheet.col_values(13)
    teamOverallColumn = standingsworksheet.col_values(14)
    for i in range (28, 35):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Sun Belt standings from CHEFF

"""
def parseSBC():
    post = "----------------------\n**Sun Belt**\n----------------------\n----------------------\nEast\n----------------------\n"
    teamColumn = standingsworksheet.col_values(16)
    teamConferenceColumn = standingsworksheet.col_values(17)
    teamOverallColumn = standingsworksheet.col_values(18)
    for i in range (28, 34):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    teamColumn = standingsworksheet.col_values(19)
    teamConferenceColumn = standingsworksheet.col_values(20)
    teamOverallColumn = standingsworksheet.col_values(21)
    for i in range (28, 34):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Big 12 standings from CHEFF

"""
def parseBig12():
    post = "----------------------\n**Big 12**\n----------------------\n"
    teamColumn = standingsworksheet.col_values(2)
    teamConferenceColumn = standingsworksheet.col_values(3)
    teamOverallColumn = standingsworksheet.col_values(4)
    for i in range (38, 43):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    teamColumn = standingsworksheet.col_values(5)
    teamConferenceColumn = standingsworksheet.col_values(6)
    teamOverallColumn = standingsworksheet.col_values(7)
    for i in range (38, 43):
        team = teamColumn[i].strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Independents standings from CHEFF

"""
def parseIndependents():
    post = "----------------------\n**Independents**\n----------------------\n"
    teamColumn = standingsworksheet.col_values(9)
    teamOverallColumn = standingsworksheet.col_values(11)
    for i in range (38, 42):
        team = teamColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + "\n"
        i += 1
    return post

"""
Get the America East standings from 1212.one

"""
def parseAmericaEast():
    post = "----------------------\n**America East**\n----------------------\n----------------------\nTri-State\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (3, 9):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nNew England\n----------------------\n"
    for i in range (3, 9):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Atlantic Sun standings from 1212.one

"""
def parseAtlanticSun():
    post = "----------------------\n**Atlantic Sun**\n----------------------\n----------------------\nDusk\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (20, 27):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nDawn\n----------------------\n"
    for i in range (28, 35):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Big Sky standings from 1212.one

"""
def parseBigSky():
    post = "----------------------\n**Big Sky**\n----------------------\n----------------------\nSouth\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (39, 46):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nNorth\n----------------------\n"
    for i in range (47, 54):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Carolina Football Conference standings from 1212.one

"""
def parseCFC():
    post = "--------------------------------------------\n**Carolina Football Conference**\n--------------------------------------------\n----------------------\nNorth\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (58, 64):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nSouth\n----------------------\n"
    for i in range (65, 71):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Colonial standings from 1212.one

"""
def parseColonial():
    post = "----------------------\n**Colonial**\n----------------------\n----------------------\nSouth\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (75, 81):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nNorth\n----------------------\n"
    for i in range (82, 88):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Delta Intercollegiate standings from 1212.one

"""
def parseDelta():
    post = "--------------------------------------------\n**Delta Intercollegiate**\n--------------------------------------------\n----------------------\nMississippi Valley\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (92, 100):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nTennessee Valley\n----------------------\n"
    for i in range (82, 88):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Ivy League standings from 1212.one

"""
def parseIvy():
    post = "----------------------\n**Ivy League**\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(6)
    for i in range (113, 121):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Mid-Atlantic standings from 1212.one

"""
def parseMidAtlantic():
    post = "----------------------\n**Mid Atlantic**\n----------------------\n----------------------\nAtlantic\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (125, 131):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nAdirondack\n----------------------\n"
    for i in range (132, 138):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Missouri Valley standings from 1212.one

"""
def parseMVC():
    post = "--------------------------------------------\n**Missouri Valley**\n-----------------------------------------\n----------------------\nPrairie\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(9)
    for i in range (142, 149):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    post = post + "\n----------------------\nMetro\n----------------------\n"
    for i in range (150, 157):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post

"""
Get the Southland standings from 1212.one

"""
def parseSouthland():
    post = "----------------------\n**Southland**\n----------------------\n"
    teamColumn = fcsstandingsworksheet.col_values(2)
    teamConferenceColumn = fcsstandingsworksheet.col_values(3)
    teamOverallColumn = fcsstandingsworksheet.col_values(6)
    for i in range (161,175):
        team = teamColumn[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conferenceRecord = teamConferenceColumn[i].strip()
        overallRecord = teamOverallColumn[i].strip()
        post = post + " " + team + " " + overallRecord + " (" + conferenceRecord + ")\n"
        i += 1
    return post
    

"""
Get the stadings data to post on Discord

"""
def getStandingsData(conference):
    if (conference == "ACC" or conference == "acc"):
        return parseACC()
    elif (conference == "American" or conference == "american" or conference == "AAC" or conference == "aac"):
        return parseAAC()
    elif (conference == "Big Ten" or conference == "big ten" or conference == "B1G" or conference == "b1g"
    or conference == "Big 10" or conference == "big 10"):
        return parseBigTen()
    elif (conference == "Conference USA" or conference == "conference usa" or conference == "CUSA" or conference == "cusa"
    or conference == "C-USA" or conference == "c-usa"):
        return parseCUSA()
    elif (conference == "MAC" or conference == "mac"):
        return parseMAC()
    elif (conference == "Mountain West" or conference == "mountain west" or conference == "MWC" or conference == "mwc"):
        return parseMWC()
    elif (conference == "Pac-12" or conference == "pac-12" or conference == "PAC-12" or conference == "Pac 12"
    or conference == "pac 12" or conference == "PAC 12"):
        return parsePac12()
    elif (conference == "SEC" or conference == "sec"):
        return parseSEC()
    elif (conference == "Sun Belt" or conference == "sun belt" or conference == "SBC" or conference == "sbc"):
        return parseSBC()
    elif (conference == "Big 12" or conference == "big 12" or conference == "Big XII" or conference == "big xii"):
        return parseBig12()
    elif (conference == "Independents" or conference == "independents" or conference == "Independent" or conference == "idependents"):
        return parseIndependents()
    elif (conference == "America East" or conference == "america east"):
        return parseAmericaEast()
    elif (conference == "Atlantic Sun" or conference == "atlantic sun"):
        return parseAtlanticSun()
    elif (conference == "Big Sky" or conference == "big sky"):
        return parseBigSky()
    elif (conference == "Carolina" or conference == "carolina" or conference == "Carolina Football Conference" or conference == "carolina football conference"
          or conference == "CFC" or conference == "cfc"):
        return parseCFC()
    elif (conference == "Colonial" or conference == "colonial"):
        return parseColonial()
    elif (conference == "Delta" or conference == "delta" or conference == "Delta Intercollegiate" or conference == "delta intercollegiate"):
        return parseDelta()
    elif (conference == "Ivy" or conference == "ivy" or conference == "Ivy League" or conference == "ivy league"):
        return parseIvy()
    elif (conference == "Mid Atlantic" or conference == "mid atlantic" or conference == "Mid-Atlantic" or conference == "mid-atlantic"):
        return parseMidAtlantic()
    elif (conference == "Missouri Valley" or conference == "missouri valley" or conference == "MVC" or conference == "mvc"):
        return parseMVC()
    elif (conference == "Southland" or conference == "southland"):
        return parseSouthland()
    else:
        return "Conference not found"
 
"""
Parse the rankings worksheet post

"""
def parseRankingsWorksheet(numCol, teamCol, valueCol, post):
    ranks = rankingsworksheet.col_values(numCol)
    teams = rankingsworksheet.col_values(teamCol)
    values = rankingsworksheet.col_values(valueCol)
    i = 4
    for team in teams[4:-1]:
        value = values[i]
        rank = ranks[i]
        if((int(rank)) > 25):
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post

"""
Parse the SOSMOVR worksheet from Zen Sunshine and output the post

"""
def parseSOSMOVRWorksheet(numCol, teamCol, valueCol, post):
    ranks = sosmovrworksheet.col_values(numCol)
    teams = sosmovrworksheet.col_values(teamCol)
    values = sosmovrworksheet.col_values(valueCol)
    i = 1
    for team in teams[1:-1]:
        value = values[i]
        rank = ranks[i]
        if((int(rank)) > 25):
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post

"""
Parse the composite worksheet

"""
def parseCompositeData(numCol, teamCol, valueCol, post):
    ranks = compositeworksheet.col_values(numCol)
    teams = compositeworksheet.col_values(teamCol)
    values = compositeworksheet.col_values(valueCol)
    i = 4
    for team in teams[4:-1]:
        value = values[i]
        rank = ranks[i]
        if((int(rank)) > 25):
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post

"""
Parse the speed worksheet 

"""
def parseSpeedData(numCol, teamCol, valueCol, post):
    ranks = speedworksheet.col_values(numCol)
    teams = speedworksheet.col_values(teamCol)
    values = speedworksheet.col_values(valueCol)
    i = 2
    for team in teams[2:-1]:
        value = values[i]
        rank = ranks[i]
        if((int(rank)) > 25):
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post
    
"""
Get the rankings data to post on Discord

"""      
def getRankingsData(r, request):
    try:
        if(request.lower() == "fbs coaches" or request.lower() == "fbs coaches poll"):
            return getCoachesPollData(r, "FBS")
            
        elif(request.lower() == "fcs coaches" or request.lower() == "fcs coaches poll"):
            return getCoachesPollData(r, "FCS")
        if(request.lower() == "coaches" or request.lower() == "coaches poll"):
            return "Please specify whether you want FBS or FCS coaches poll data"
        if(request.lower() == "fbs" or request.lower() == "fcs"):
            return "Please be more specific"
        if("committee" in request.lower() or "playoff" in request.lower()):
            return "This request is not available right now"
        if(request.lower() == "fbs elo"):
            fbsColumn = fbsworksheet.col_values(2)
            fbsEloColumn = fbsworksheet.col_values(3)
            i = 1
            post = ("-----------------------\n**FBS Elo Rankings**\n-----------------------\n")
            for team in fbsColumn[1:26]:
                elo = fbsEloColumn[i]
                post = post + "#" + str(i) + " " + team.strip() + " " + elo.strip() + "\n"
                i = i + 1
            return post
        if(request.lower() == "fcs elo"):
            fcsColumn = fcsworksheet.col_values(4)
            fcsEloColumn = fcsworksheet.col_values(1)
            i = 1
            post = ("-----------------------\n**FCS Elo Rankings**\n-----------------------\n")
            for team in fcsColumn[1:26]:
                if("(" in team):
                    team = team.split("(")[0]
                    team = team.strip()
                elo = fcsEloColumn[i]
                post = post + "#" + str(i) + " " + team.strip() + " " + elo.strip() + "\n"
                i = i + 1
            return post
        if(request.lower() == "mov"):
            post = ("-----------------------\n**FBS MoV Rankings**\n-----------------------\n")
            return parseRankingsWorksheet(2, 3, 4, post)
        if(request.lower() == "scoring offense" or request.lower() == "offense"):
            post = ("--------------------------------------------\n**FBS Scoring Offense Rankings**\n--------------------------------------------\n")
            return parseRankingsWorksheet(10, 11, 12, post)
        if(request.lower() == "scoring defense" or request.lower() == "defense"):
            post = ("--------------------------------------------\n**FBS Scoring Defense Rankings**\n--------------------------------------------\n")
            return parseRankingsWorksheet(14, 15, 16, post)
        if(request.lower() == "sosmovr" or request.lower() == "smr" or request.lower() == "sauce mover"):
            post = ("--------------------------------------------\n**FBS SOSMOVR**\n--------------------------------------------\n")
            return parseSOSMOVRWorksheet(2, 3, 4, post)
        if(request.lower() == "eqw"):
            post = ("--------------------------------------------\n**FBS EQW**\n--------------------------------------------\n")
            return parseSOSMOVRWorksheet(7, 8, 9, post)
        if(request.lower() == "composite"):
            post = ("--------------------------------------------\n**Composite**\n--------------------------------------------\n")
            return parseCompositeData(2, 3, 4, post)
        if(request.lower() == "colley" or request.lower() == "colley matrix"):
            post = ("--------------------------------------------\n**Colley Matrix**\n--------------------------------------------\n")
            return parseCompositeData(13, 14, 15, post)
        if(request.lower() == "adjusted strength rating" or request.lower() == "adjusted strength" or request.lower() == "asr"):
            post = ("--------------------------------------------\n**Adjusted Strength Rating**\n--------------------------------------------\n")
            return parseCompositeData(17, 18, 19, post)
        if(request.lower() == "adjusted speed" or request.lower() == "speed"):
            post = ("--------------------------------------------\n**Adjusted Speed**\n--------------------------------------------\n")
            return parseSpeedData(2, 3, 4, post)
        if(request.lower() == "raw speed"):
            post = ("--------------------------------------------\n**Raw Speed**\n--------------------------------------------\n")
            return parseSpeedData(10, 11, 12, post)
        return "Invalid command. Please try again."
    except:
        return "There was an error in contacting Google Sheets, please try again."
    
        
    
    
            
            
        
        
    