import gspread
from oauth2client.service_account import ServiceAccountCredentials

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


"""
Get Elo data from both FBS and FCS sheets

"""
def getEloData():
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
 
"""
Get Hex Color data for both FBS and FCS teams

"""
def getColorData():
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