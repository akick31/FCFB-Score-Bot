<<<<<<< HEAD
import gspread
import xlrd
from oauth2client.service_account import *
from poll_data import *

"""
Handle contacting Google Sheets and getting information from the document

@author: apkick
"""

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('FCFBRollCallBot-2d263a255851.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZFi4MqxWX84-VdIiWjJmuvB8f80lfKNkffeKcdJKtAU/edit#gid=1106595477')
fbs_worksheet = sh.worksheet("Season 7 Rankings (All-Time)")

file_location = "FCSElo.xlsx"
fcs_excel = xlrd.open_workbook(file_location)
sheet = fcs_excel.sheet_by_name('sheet')

sh3 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Xx6l7oLRZe8Y0Ia1pHDSeCYjXg260skf8YMNoXkp7Hc/edit#gid=0')
standingsWorksheet = sh3.worksheet("Standings")
rankingsWorksheet = sh3.worksheet("Rankings")
composite_worksheet = sh3.worksheet("Composite")

sh4 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1IrBBMKApJVYlU10wCOKp_oW3wvQfFT-xTC_A6EHJlzU/edit?usp=sharing')
fcs_standings_worksheet = sh4.worksheet("Sheet1")

sh5 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1GDDwQ2FpZIgGoDdZoRNbBg8IyQir2-WZriz8bHHXbSE/edit?usp=sharing')
sosmovr_worksheet = sh5.worksheet("SOSMOVR")

sh6 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZAt2PjbwHCoWaQZY6jsQRHUK9t6xHZCxa1wn1W9Kt9E/edit?usp=sharing')
speed_worksheet = sh6.worksheet("Quickest Team Ranking")

sh7 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nCoC6j9GbA3AqJbQ5rCZQICrWEVRdvDqXe5ZJnjAGXU/edit#gid=155279901')
start_games_worksheet = sh7.worksheet("Weekly Blocks")


"""
Get Elo data from both FBS and FCS sheets

"""


def get_elo_data():
    try:
        team_elo_column = []
        elo_data_column = []
        fbs_column = fbs_worksheet.col_values(2)
        fbs_column.pop(0)
        fcs_column = get_excel_data(3)
        fcs_column.pop(0)
        team_elo_column.extend(fbs_column)
        team_elo_column.extend(fcs_column)

        fbs_elo_column = fbs_worksheet.col_values(3)
        fbs_elo_column.pop(0)
        fcs_elo_column = get_excel_data(0)
        fcs_elo_column.pop(0)
        elo_data_column.extend(fbs_elo_column)
        elo_data_column.extend(fcs_elo_column)
        
        return {1: team_elo_column, 2: elo_data_column}
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement

   
    
"""
Get the ACC standings from CHEFF

"""


def parse_acc():
    post = ("----------------------\n**ACC**\n----------------------\n" +
           "----------------------\nAtlantic\n----------------------\n")
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nCoastal\n----------------------\n"
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the AAC standings from CHEFF

"""


def parse_aac():
    post = "----------------------\n**American**\n----------------------\n----------------------\nEast\n----------------------\n"
    team_column = standingsWorksheet.col_values(9)
    team_conference_column = standingsWorksheet.col_values(10)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(6, 12):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(12)
    team_conference_column = standingsWorksheet.col_values(13)
    team_overall_column = standingsWorksheet.col_values(14)
    for i in range(6, 12):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Big 10 standings from CHEFF

"""


def parse_bigten():
    post = ("----------------------\n**Big Ten**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(16)
    team_conference_column = standingsWorksheet.col_values(17)
    team_overall_column = standingsWorksheet.col_values(18)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(19)
    team_conference_column = standingsWorksheet.col_values(20)
    team_overall_column = standingsWorksheet.col_values(21)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Pac 12 standings from CHEFF

"""


def parse_pac12():
    post = ("----------------------\n**Pac-12**\n----------------------\n" + 
            "----------------------\nNorth\n----------------------\n")
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nSouth\n----------------------\n"
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the CUSA standings from CHEFF

"""


def parse_cusa():
    post = ("----------------------\n**Conference USA**\n----------------------\n" +
           "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(17, 24):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(17, 24):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the MAC standings from CHEFF

"""


def parse_mac():
    post = ("----------------------\n**MAC**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(9)
    team_conference_column = standingsWorksheet.col_values(10)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(12)
    team_conference_column = standingsWorksheet.col_values(13)
    team_overall_column = standingsWorksheet.col_values(14)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Mountain West standings from CHEFF

"""


def parse_mwc():
    post = ("----------------------\n**Mountain West**\n----------------------\n" +
            "----------------------\nMountain\n----------------------\n")
    team_column = standingsWorksheet.col_values(16)
    team_conference_column = standingsWorksheet.col_values(17)
    team_overall_column = standingsWorksheet.col_values(18)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(19)
    team_conference_column = standingsWorksheet.col_values(20)
    team_overall_column = standingsWorksheet.col_values(21)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the SEC standings from CHEFF

"""


def parse_sec():
    post = ("----------------------\n**SEC**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(9)
    team_conference_column = standingsWorksheet.col_values(10)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(28, 35):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(12)
    team_conference_column = standingsWorksheet.col_values(13)
    team_overall_column = standingsWorksheet.col_values(14)
    for i in range(28, 35):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Sun Belt standings from CHEFF

"""


def parse_sbc():
    post = ("----------------------\n**Sun Belt**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(16)
    team_conference_column = standingsWorksheet.col_values(17)
    team_overall_column = standingsWorksheet.col_values(18)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(19)
    team_conference_column = standingsWorksheet.col_values(20)
    team_overall_column = standingsWorksheet.col_values(21)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Big 12 standings from CHEFF

"""


def parse_big12():
    post = "----------------------\n**Big 12**\n----------------------\n"
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(38, 43):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(38, 43):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Independents standings from CHEFF

"""


def parse_independents():
    post = "----------------------\n**Independents**\n----------------------\n"
    team_column = standingsWorksheet.col_values(9)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(38, 42):
        team = team_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + "\n"
        i += 1
    return post


"""
Get the America East standings from 1212.one

"""


def parse_americaeast():
    post = ("----------------------\n**America East**\n----------------------\n" +
            "----------------------\nTri-State\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(3, 9):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nNew England\n----------------------\n"
    for i in range(3, 9):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Atlantic Sun standings from 1212.one

"""


def parse_atlanticsun():
    post = ("----------------------\n**Atlantic Sun**\n----------------------\n" +
            "----------------------\nDusk\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(20, 27):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nDawn\n----------------------\n"
    for i in range(28, 35):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Big Sky standings from 1212.one

"""


def parse_bigsky():
    post = ("----------------------\n**Big Sky**\n----------------------\n" +
           "----------------------\nSouth\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(39, 46):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nNorth\n----------------------\n"
    for i in range(47, 54):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Carolina Football Conference standings from 1212.one

"""


def parse_cfc():
    post = ("--------------------------------------------\n**Carolina Football Conference**\n--------------------" + 
            "------------------------\n" +
            "----------------------\nNorth\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(58, 64):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nSouth\n----------------------\n"
    for i in range(65, 71):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Colonial standings from 1212.one

"""


def parse_colonial():
    post = ("----------------------\n**Colonial**\n----------------------\n" +
           "----------------------\nSouth\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(75, 81):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nNorth\n----------------------\n"
    for i in range(82, 88):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post

"""
Get the Delta Intercollegiate standings from 1212.one

"""
def parse_delta():
    post = ("--------------------------------------------\n**Delta Intercollegiate**\n-------------------" + 
            "-------------------------\n" +
            "----------------------\nMississippi Valley\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(92, 100):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nTennessee Valley\n----------------------\n"
    for i in range(82, 88):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Ivy League standings from 1212.one

"""


def parse_ivy():
    post = "----------------------\n**Ivy League**\n----------------------\n"
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(6)
    for i in range(113, 121):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Mid-Atlantic standings from 1212.one

"""


def parse_midatlantic():
    post = ("----------------------\n**Mid Atlantic**\n----------------------\n" +
            "----------------------\nAtlantic\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(125, 131):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nAdirondack\n----------------------\n"
    for i in range(132, 138):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post

"""
Get the Missouri Valley standings from 1212.one

"""
def parse_mvc():
    post = ("--------------------------------------------\n**Missouri Valley**\n-----------------------------------------\n" + \
           "----------------------\nPrairie\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(142, 149):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nMetro\n----------------------\n"
    for i in range(150, 157):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Southland standings from 1212.one

"""


def parse_southland():
    post = "----------------------\n**Southland**\n----------------------\n"
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(6)
    for i in range(161,175):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post
    

"""
Get the stadings data to post on Discord

"""


def get_standings_data(conference):
    conference = conference.lower()
    try:
        if conference == "acc":
            return parse_acc()
        elif conference == "american" or conference == "aac":
            return parse_aac()
        elif conference == "big ten" or conference == "b1g" or conference == "big 10" or conference == "b10":
            return parse_bigten()
        elif conference == "conference usa" or conference == "cusa" or conference == "c-usa":
            return parse_cusa()
        elif conference == "mac":
            return parse_mac()
        elif conference == "mountain west" or conference == "mwc":
            return parse_mwc()
        elif conference == "pac-12" or conference == "pac 12":
            return parse_pac12()
        elif conference == "sec":
            return parse_sec()
        elif conference == "sun belt" or conference == "sbc":
            return parse_sbc()
        elif conference == "big 12" or conference == "big xii" or conference == "b12":
            return parse_big12()
        elif conference == "independents" or conference == "independent":
            return parse_independents()
        elif conference == "america east":
            return parse_americaeast()
        elif conference == "atlantic sun":
            return parse_atlanticsun()
        elif conference == "big sky":
            return parse_bigsky()
        elif conference == "carolina" or conference == "carolina football conference" or conference == "cfc":
            return parse_cfc()
        elif conference == "colonial":
            return parse_colonial()
        elif conference == "delta" or conference == "delta intercollegiate":
            return parse_delta()
        elif conference == "ivy" or conference == "ivy league":
            return parse_ivy()
        elif conference == "mid atlantic" or conference == "mid-atlantic":
            return parse_midatlantic()
        elif conference == "missouri valley" or conference == "mvc":
            return parse_mvc()
        elif conference == "southland":
            return parse_southland()
        else:
            return "Conference not found"
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement
 
 
"""
Parse the rankings worksheet post

"""


def parse_rankings_worksheet(num_col, team_col, value_col, post):
    ranks = rankingsWorksheet.col_values(num_col)
    teams = rankingsWorksheet.col_values(team_col)
    values = rankingsWorksheet.col_values(value_col)
    i = 4
    for team in teams[4:-1]:
        value = values[i]
        rank = ranks[i]
        if int(rank) > 25:
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post


"""
Parse the SOSMOVR worksheet from Zen Sunshine and output the post

"""


def parse_sosmovr_worksheet(num_col, team_col, value_col, post):
    ranks = sosmovr_worksheet.col_values(num_col)
    teams = sosmovr_worksheet.col_values(team_col)
    values = sosmovr_worksheet.col_values(value_col)
    i = 1
    for team in teams[1:-1]:
        value = values[i]
        rank = ranks[i]
        if int(rank) > 25:
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post


"""
Parse the composite worksheet

"""


def parse_composite_data(num_col, team_col, value_col, post):
    try:
        ranks = composite_worksheet.col_values(num_col)
        teams = composite_worksheet.col_values(team_col)
        values = composite_worksheet.col_values(value_col)
        i = 4
        for team in teams[4:-1]:
            value = values[i]
            rank = ranks[i]
            if int(rank) > 25:
                break
            post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
            i = i + 1
        return post
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement


"""
Parse the speed worksheet 

"""


def parse_speed_data(num_col, team_col, value_col, post):
    ranks = speed_worksheet.col_values(num_col)
    teams = speed_worksheet.col_values(team_col)
    values = speed_worksheet.col_values(value_col)
    i = 2
    for team in teams[2:-1]:
        value = values[i]
        rank = ranks[i]
        if int(rank) > 25:
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post
    
    
"""
Get the rankings data to post on Discord

"""      


def get_rankings_data(r, request):
    try:
        if request.lower() == "fbs coaches" or request.lower() == "fbs coaches poll":
            return get_coaches_poll_data(r, "FBS")
            
        elif request.lower() == "fcs coaches" or request.lower() == "fcs coaches poll":
            return get_coaches_poll_data(r, "FCS")
        if request.lower() == "coaches" or request.lower() == "coaches poll":
            return "Please specify whether you want FBS or FCS coaches poll data"
        if request.lower() == "fbs" or request.lower() == "fcs":
            return "Please be more specific"
        if "committee" in request.lower() or "playoff" in request.lower():
            return "This request is not available right now"
        if request.lower() == "fbs elo":
            fbs_column = fbs_worksheet.col_values(2)
            fbs_elo_column = fbs_worksheet.col_values(3)
            i = 1
            post = "-----------------------\n**FBS Elo Rankings**\n-----------------------\n"
            for team in fbs_column[1:26]:
                elo = fbs_elo_column[i]
                post = post + "#" + str(i) + " " + team.strip() + " " + elo.strip() + "\n"
                i = i + 1
            return post
        if request.lower() == "fcs elo":
            fcs_column = get_excel_data(3)
            fcs_elo_column = get_excel_data(0)
            i = 1
            post = "-----------------------\n**FCS Elo Rankings**\n-----------------------\n"
            for team in fcs_column[1:26]:
                if "(" in team:
                    team = team.split("(")[0]
                    team = team.strip()
                elo = fcs_elo_column[i]
                post = post + "#" + str(i) + " " + team.strip() + " " + elo.strip() + "\n"
                i = i + 1
            return post
        if request.lower() == "mov":
            post = "-----------------------\n**FBS MoV Rankings**\n-----------------------\n"
            return parse_rankings_worksheet(2, 3, 4, post)
        if request.lower() == "scoring offense" or request.lower() == "offense":
            post = "--------------------------------------------\n**FBS Scoring Offense Rankings**\n--------------------------------------------\n"
            return parse_rankings_worksheet(10, 11, 12, post)
        if request.lower() == "scoring defense" or request.lower() == "defense":
            post = "--------------------------------------------\n**FBS Scoring Defense Rankings**\n--------------------------------------------\n"
            return parse_rankings_worksheet(14, 15, 16, post)
        if request.lower() == "sosmovr" or request.lower() == "smr" or request.lower() == "sauce mover":
            post = "--------------------------------------------\n**FBS SOSMOVR**\n--------------------------------------------\n"
            return parse_sosmovr_worksheet(2, 3, 4, post)
        if request.lower() == "eqw":
            post = "--------------------------------------------\n**FBS EQW**\n--------------------------------------------\n"
            return parse_sosmovr_worksheet(7, 8, 9, post)
        if request.lower() == "composite":
            post = "--------------------------------------------\n**Composite**\n--------------------------------------------\n"
            return parse_composite_data(2, 3, 4, post)
        if request.lower() == "colley" or request.lower() == "colley matrix":
            post = "--------------------------------------------\n**Colley Matrix**\n--------------------------------------------\n"
            return parse_composite_data(13, 14, 15, post)
        if request.lower() == "adjusted strength rating" or request.lower() == "adjusted strength" or request.lower() == "asr":
            post = "--------------------------------------------\n**Adjusted Strength Rating**\n--------------------------------------------\n"
            return parse_composite_data(17, 18, 19, post)
        if request.lower() == "adjusted speed" or request.lower() == "speed":
            post = "--------------------------------------------\n**Adjusted Speed**\n--------------------------------------------\n"
            return parse_speed_data(2, 3, 4, post)
        if request.lower() == "raw speed":
            post = "--------------------------------------------\n**Raw Speed**\n--------------------------------------------\n"
            return parse_speed_data(10, 11, 12, post)
        return "Invalid command. Please try again."
    except Exception as e:
        return_statement = "**Rankings retrieval error**\n\nThe following error occured: " + str(e)
        return return_statement


"""
Get a column from the excel spreadsheet

"""


def get_excel_data(column):
    column_vals = []
    for row_num in range(sheet.nrows):
        column_vals.append(str(sheet.cell(row_num, column).value))
    return column_vals       
    
    
"""
Get the commands to start a game and return it as a list


"""


def parse_game_start_commands():
    try:
        commands = start_games_worksheet.col_values(2)
        return commands
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement
            
        
        
=======
import gspread
import xlrd
from oauth2client.service_account import *
from poll_data import *

"""
Handle contacting Google Sheets and getting information from the document

@author: apkick
"""

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('FCFBRollCallBot-2d263a255851.json', scope)
gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZFi4MqxWX84-VdIiWjJmuvB8f80lfKNkffeKcdJKtAU/edit#gid=1106595477')
fbs_worksheet = sh.worksheet("Season 7 Rankings (All-Time)")

file_location = "FCSElo.xlsx"
fcs_excel = xlrd.open_workbook(file_location)
sheet = fcs_excel.sheet_by_name('sheet')

sh3 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Xx6l7oLRZe8Y0Ia1pHDSeCYjXg260skf8YMNoXkp7Hc/edit#gid=0')
standingsWorksheet = sh3.worksheet("Standings")
rankingsWorksheet = sh3.worksheet("Rankings")
composite_worksheet = sh3.worksheet("Composite")

sh4 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1IrBBMKApJVYlU10wCOKp_oW3wvQfFT-xTC_A6EHJlzU/edit?usp=sharing')
fcs_standings_worksheet = sh4.worksheet("Sheet1")

sh5 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1GDDwQ2FpZIgGoDdZoRNbBg8IyQir2-WZriz8bHHXbSE/edit?usp=sharing')
sosmovr_worksheet = sh5.worksheet("SOSMOVR")

sh6 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ZAt2PjbwHCoWaQZY6jsQRHUK9t6xHZCxa1wn1W9Kt9E/edit?usp=sharing')
speed_worksheet = sh6.worksheet("Quickest Team Ranking")

sh7 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1nCoC6j9GbA3AqJbQ5rCZQICrWEVRdvDqXe5ZJnjAGXU/edit#gid=155279901')
start_games_worksheet = sh7.worksheet("Weekly Blocks")


"""
Get Elo data from both FBS and FCS sheets

"""


def get_elo_data():
    try:
        team_elo_column = []
        elo_data_column = []
        fbs_column = fbs_worksheet.col_values(2)
        fbs_column.pop(0)
        fcs_column = get_excel_data(3)
        fcs_column.pop(0)
        team_elo_column.extend(fbs_column)
        team_elo_column.extend(fcs_column)

        fbs_elo_column = fbs_worksheet.col_values(3)
        fbs_elo_column.pop(0)
        fcs_elo_column = get_excel_data(0)
        fcs_elo_column.pop(0)
        elo_data_column.extend(fbs_elo_column)
        elo_data_column.extend(fcs_elo_column)
        
        return {1: team_elo_column, 2: elo_data_column}
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement

   
    
"""
Get the ACC standings from CHEFF

"""


def parse_acc():
    post = ("----------------------\n**ACC**\n----------------------\n" +
           "----------------------\nAtlantic\n----------------------\n")
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nCoastal\n----------------------\n"
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the AAC standings from CHEFF

"""


def parse_aac():
    post = "----------------------\n**American**\n----------------------\n----------------------\nEast\n----------------------\n"
    team_column = standingsWorksheet.col_values(9)
    team_conference_column = standingsWorksheet.col_values(10)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(6, 12):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(12)
    team_conference_column = standingsWorksheet.col_values(13)
    team_overall_column = standingsWorksheet.col_values(14)
    for i in range(6, 12):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Big 10 standings from CHEFF

"""


def parse_bigten():
    post = ("----------------------\n**Big Ten**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(16)
    team_conference_column = standingsWorksheet.col_values(17)
    team_overall_column = standingsWorksheet.col_values(18)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(19)
    team_conference_column = standingsWorksheet.col_values(20)
    team_overall_column = standingsWorksheet.col_values(21)
    for i in range(6, 13):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Pac 12 standings from CHEFF

"""


def parse_pac12():
    post = ("----------------------\n**Pac-12**\n----------------------\n" + 
            "----------------------\nNorth\n----------------------\n")
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nSouth\n----------------------\n"
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the CUSA standings from CHEFF

"""


def parse_cusa():
    post = ("----------------------\n**Conference USA**\n----------------------\n" +
           "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(17, 24):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(17, 24):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the MAC standings from CHEFF

"""


def parse_mac():
    post = ("----------------------\n**MAC**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(9)
    team_conference_column = standingsWorksheet.col_values(10)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(12)
    team_conference_column = standingsWorksheet.col_values(13)
    team_overall_column = standingsWorksheet.col_values(14)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Mountain West standings from CHEFF

"""


def parse_mwc():
    post = ("----------------------\n**Mountain West**\n----------------------\n" +
            "----------------------\nMountain\n----------------------\n")
    team_column = standingsWorksheet.col_values(16)
    team_conference_column = standingsWorksheet.col_values(17)
    team_overall_column = standingsWorksheet.col_values(18)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(19)
    team_conference_column = standingsWorksheet.col_values(20)
    team_overall_column = standingsWorksheet.col_values(21)
    for i in range(17, 23):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the SEC standings from CHEFF

"""


def parse_sec():
    post = ("----------------------\n**SEC**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(9)
    team_conference_column = standingsWorksheet.col_values(10)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(28, 35):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(12)
    team_conference_column = standingsWorksheet.col_values(13)
    team_overall_column = standingsWorksheet.col_values(14)
    for i in range(28, 35):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Sun Belt standings from CHEFF

"""


def parse_sbc():
    post = ("----------------------\n**Sun Belt**\n----------------------\n" +
            "----------------------\nEast\n----------------------\n")
    team_column = standingsWorksheet.col_values(16)
    team_conference_column = standingsWorksheet.col_values(17)
    team_overall_column = standingsWorksheet.col_values(18)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nWest\n----------------------\n"
    team_column = standingsWorksheet.col_values(19)
    team_conference_column = standingsWorksheet.col_values(20)
    team_overall_column = standingsWorksheet.col_values(21)
    for i in range(28, 34):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Big 12 standings from CHEFF

"""


def parse_big12():
    post = "----------------------\n**Big 12**\n----------------------\n"
    team_column = standingsWorksheet.col_values(2)
    team_conference_column = standingsWorksheet.col_values(3)
    team_overall_column = standingsWorksheet.col_values(4)
    for i in range(38, 43):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    team_column = standingsWorksheet.col_values(5)
    team_conference_column = standingsWorksheet.col_values(6)
    team_overall_column = standingsWorksheet.col_values(7)
    for i in range(38, 43):
        team = team_column[i].strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Independents standings from CHEFF

"""


def parse_independents():
    post = "----------------------\n**Independents**\n----------------------\n"
    team_column = standingsWorksheet.col_values(9)
    team_overall_column = standingsWorksheet.col_values(11)
    for i in range(38, 42):
        team = team_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + "\n"
        i += 1
    return post


"""
Get the America East standings from 1212.one

"""


def parse_americaeast():
    post = ("----------------------\n**America East**\n----------------------\n" +
            "----------------------\nTri-State\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(3, 9):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nNew England\n----------------------\n"
    for i in range(3, 9):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Atlantic Sun standings from 1212.one

"""


def parse_atlanticsun():
    post = ("----------------------\n**Atlantic Sun**\n----------------------\n" +
            "----------------------\nDusk\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(20, 27):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nDawn\n----------------------\n"
    for i in range(28, 35):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Big Sky standings from 1212.one

"""


def parse_bigsky():
    post = ("----------------------\n**Big Sky**\n----------------------\n" +
           "----------------------\nSouth\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(39, 46):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nNorth\n----------------------\n"
    for i in range(47, 54):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Carolina Football Conference standings from 1212.one

"""


def parse_cfc():
    post = ("--------------------------------------------\n**Carolina Football Conference**\n--------------------" + 
            "------------------------\n" +
            "----------------------\nNorth\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(58, 64):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nSouth\n----------------------\n"
    for i in range(65, 71):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Colonial standings from 1212.one

"""


def parse_colonial():
    post = ("----------------------\n**Colonial**\n----------------------\n" +
           "----------------------\nSouth\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(75, 81):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nNorth\n----------------------\n"
    for i in range(82, 88):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post

"""
Get the Delta Intercollegiate standings from 1212.one

"""
def parse_delta():
    post = ("--------------------------------------------\n**Delta Intercollegiate**\n-------------------" + 
            "-------------------------\n" +
            "----------------------\nMississippi Valley\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(92, 100):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nTennessee Valley\n----------------------\n"
    for i in range(82, 88):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Ivy League standings from 1212.one

"""


def parse_ivy():
    post = "----------------------\n**Ivy League**\n----------------------\n"
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(6)
    for i in range(113, 121):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Mid-Atlantic standings from 1212.one

"""


def parse_midatlantic():
    post = ("----------------------\n**Mid Atlantic**\n----------------------\n" +
            "----------------------\nAtlantic\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(125, 131):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nAdirondack\n----------------------\n"
    for i in range(132, 138):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post

"""
Get the Missouri Valley standings from 1212.one

"""
def parse_mvc():
    post = ("--------------------------------------------\n**Missouri Valley**\n-----------------------------------------\n" + \
           "----------------------\nPrairie\n----------------------\n")
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(9)
    for i in range(142, 149):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    post = post + "\n----------------------\nMetro\n----------------------\n"
    for i in range(150, 157):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post


"""
Get the Southland standings from 1212.one

"""


def parse_southland():
    post = "----------------------\n**Southland**\n----------------------\n"
    team_column = fcs_standings_worksheet.col_values(2)
    team_conference_column = fcs_standings_worksheet.col_values(3)
    team_overall_column = fcs_standings_worksheet.col_values(6)
    for i in range(161,175):
        team = team_column[i].split(" ")[:-1]
        team = ' '.join(team).strip()
        conference_record = team_conference_column[i].strip()
        overall_record = team_overall_column[i].strip()
        post = post + " " + team + " " + overall_record + " (" + conference_record + ")\n"
        i += 1
    return post
    

"""
Get the stadings data to post on Discord

"""


def get_standings_data(conference):
    conference = conference.lower()
    try:
        if conference == "acc":
            return parse_acc()
        elif conference == "american" or conference == "aac":
            return parse_aac()
        elif conference == "big ten" or conference == "b1g" or conference == "big 10" or conference == "b10":
            return parse_bigten()
        elif conference == "conference usa" or conference == "cusa" or conference == "c-usa":
            return parse_cusa()
        elif conference == "mac":
            return parse_mac()
        elif conference == "mountain west" or conference == "mwc":
            return parse_mwc()
        elif conference == "pac-12" or conference == "pac 12":
            return parse_pac12()
        elif conference == "sec":
            return parse_sec()
        elif conference == "sun belt" or conference == "sbc":
            return parse_sbc()
        elif conference == "big 12" or conference == "big xii" or conference == "b12":
            return parse_big12()
        elif conference == "independents" or conference == "independent":
            return parse_independents()
        elif conference == "america east":
            return parse_americaeast()
        elif conference == "atlantic sun":
            return parse_atlanticsun()
        elif conference == "big sky":
            return parse_bigsky()
        elif conference == "carolina" or conference == "carolina football conference" or conference == "cfc":
            return parse_cfc()
        elif conference == "colonial":
            return parse_colonial()
        elif conference == "delta" or conference == "delta intercollegiate":
            return parse_delta()
        elif conference == "ivy" or conference == "ivy league":
            return parse_ivy()
        elif conference == "mid atlantic" or conference == "mid-atlantic":
            return parse_midatlantic()
        elif conference == "missouri valley" or conference == "mvc":
            return parse_mvc()
        elif conference == "southland":
            return parse_southland()
        else:
            return "Conference not found"
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement
 
 
"""
Parse the rankings worksheet post

"""


def parse_rankings_worksheet(num_col, team_col, value_col, post):
    ranks = rankingsWorksheet.col_values(num_col)
    teams = rankingsWorksheet.col_values(team_col)
    values = rankingsWorksheet.col_values(value_col)
    i = 4
    for team in teams[4:-1]:
        value = values[i]
        rank = ranks[i]
        if int(rank) > 25:
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post


"""
Parse the SOSMOVR worksheet from Zen Sunshine and output the post

"""


def parse_sosmovr_worksheet(num_col, team_col, value_col, post):
    ranks = sosmovr_worksheet.col_values(num_col)
    teams = sosmovr_worksheet.col_values(team_col)
    values = sosmovr_worksheet.col_values(value_col)
    i = 1
    for team in teams[1:-1]:
        value = values[i]
        rank = ranks[i]
        if int(rank) > 25:
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post


"""
Parse the composite worksheet

"""


def parse_composite_data(num_col, team_col, value_col, post):
    try:
        ranks = composite_worksheet.col_values(num_col)
        teams = composite_worksheet.col_values(team_col)
        values = composite_worksheet.col_values(value_col)
        i = 4
        for team in teams[4:-1]:
            value = values[i]
            rank = ranks[i]
            if int(rank) > 25:
                break
            post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
            i = i + 1
        return post
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement


"""
Parse the speed worksheet 

"""


def parse_speed_data(num_col, team_col, value_col, post):
    ranks = speed_worksheet.col_values(num_col)
    teams = speed_worksheet.col_values(team_col)
    values = speed_worksheet.col_values(value_col)
    i = 2
    for team in teams[2:-1]:
        value = values[i]
        rank = ranks[i]
        if int(rank) > 25:
            break
        post = post + "#" + rank + " " + team.strip() + " " + value.strip() + "\n"
        i = i + 1
    return post
    
    
"""
Get the rankings data to post on Discord

"""      


def get_rankings_data(r, request):
    try:
        if request.lower() == "fbs coaches" or request.lower() == "fbs coaches poll":
            return get_coaches_poll_data(r, "FBS")
            
        elif request.lower() == "fcs coaches" or request.lower() == "fcs coaches poll":
            return get_coaches_poll_data(r, "FCS")
        if request.lower() == "coaches" or request.lower() == "coaches poll":
            return "Please specify whether you want FBS or FCS coaches poll data"
        if request.lower() == "fbs" or request.lower() == "fcs":
            return "Please be more specific"
        if "committee" in request.lower() or "playoff" in request.lower():
            return "This request is not available right now"
        if request.lower() == "fbs elo":
            fbs_column = fbs_worksheet.col_values(2)
            fbs_elo_column = fbs_worksheet.col_values(3)
            i = 1
            post = "-----------------------\n**FBS Elo Rankings**\n-----------------------\n"
            for team in fbs_column[1:26]:
                elo = fbs_elo_column[i]
                post = post + "#" + str(i) + " " + team.strip() + " " + elo.strip() + "\n"
                i = i + 1
            return post
        if request.lower() == "fcs elo":
            fcs_column = get_excel_data(3)
            fcs_elo_column = get_excel_data(0)
            i = 1
            post = "-----------------------\n**FCS Elo Rankings**\n-----------------------\n"
            for team in fcs_column[1:26]:
                if "(" in team:
                    team = team.split("(")[0]
                    team = team.strip()
                elo = fcs_elo_column[i]
                post = post + "#" + str(i) + " " + team.strip() + " " + elo.strip() + "\n"
                i = i + 1
            return post
        if request.lower() == "mov":
            post = "-----------------------\n**FBS MoV Rankings**\n-----------------------\n"
            return parse_rankings_worksheet(2, 3, 4, post)
        if request.lower() == "scoring offense" or request.lower() == "offense":
            post = "--------------------------------------------\n**FBS Scoring Offense Rankings**\n--------------------------------------------\n"
            return parse_rankings_worksheet(10, 11, 12, post)
        if request.lower() == "scoring defense" or request.lower() == "defense":
            post = "--------------------------------------------\n**FBS Scoring Defense Rankings**\n--------------------------------------------\n"
            return parse_rankings_worksheet(14, 15, 16, post)
        if request.lower() == "sosmovr" or request.lower() == "smr" or request.lower() == "sauce mover":
            post = "--------------------------------------------\n**FBS SOSMOVR**\n--------------------------------------------\n"
            return parse_sosmovr_worksheet(2, 3, 4, post)
        if request.lower() == "eqw":
            post = "--------------------------------------------\n**FBS EQW**\n--------------------------------------------\n"
            return parse_sosmovr_worksheet(7, 8, 9, post)
        if request.lower() == "composite":
            post = "--------------------------------------------\n**Composite**\n--------------------------------------------\n"
            return parse_composite_data(2, 3, 4, post)
        if request.lower() == "colley" or request.lower() == "colley matrix":
            post = "--------------------------------------------\n**Colley Matrix**\n--------------------------------------------\n"
            return parse_composite_data(13, 14, 15, post)
        if request.lower() == "adjusted strength rating" or request.lower() == "adjusted strength" or request.lower() == "asr":
            post = "--------------------------------------------\n**Adjusted Strength Rating**\n--------------------------------------------\n"
            return parse_composite_data(17, 18, 19, post)
        if request.lower() == "adjusted speed" or request.lower() == "speed":
            post = "--------------------------------------------\n**Adjusted Speed**\n--------------------------------------------\n"
            return parse_speed_data(2, 3, 4, post)
        if request.lower() == "raw speed":
            post = "--------------------------------------------\n**Raw Speed**\n--------------------------------------------\n"
            return parse_speed_data(10, 11, 12, post)
        return "Invalid command. Please try again."
    except Exception as e:
        return_statement = "**Rankings retrieval error**\n\nThe following error occured: " + str(e)
        return return_statement


"""
Get a column from the excel spreadsheet

"""


def get_excel_data(column):
    column_vals = []
    for row_num in range(sheet.nrows):
        column_vals.append(str(sheet.cell(row_num, column).value))
    return column_vals       
    
    
"""
Get the commands to start a game and return it as a list


"""


def parse_game_start_commands():
    try:
        commands = start_games_worksheet.col_values(2)
        return commands
    except Exception as e:
        return_statement = "The following error occured: " + str(e)
        return return_statement
            
        
        
>>>>>>> fc08d1834828820fa06a447399d078cce40334d7
    