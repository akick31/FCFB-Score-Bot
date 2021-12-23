from sheets_functions import *

"""
Handle the colors aspect of the bot

@author: apkick
"""


"""
Get the colors for both teams playing

"""


def get_scorebug_colors(home_team, away_team):
    color_dict = get_color_data()
    if color_dict != "There was an error in contacting Google Sheets, please try again.":
        team_color_column = color_dict[1]
        color_data_column = color_dict[2]
        home_color = get_color(home_team, team_color_column, color_data_column)
        away_color = get_color(away_team, team_color_column, color_data_column)
        return {1: home_color, 2: away_color}
    else:
        return "There was an error in contacting Google Sheets, please try again."


"""
Get the colors for both teams playing

"""


def get_team_colors(home_team, away_team):
    color_dict = get_color_data()
    if color_dict != "There was an error in contacting Google Sheets, please try again.":
        team_color_column = color_dict[1]
        color_data_column = color_dict[2]
        home_color = get_color(home_team, team_color_column, color_data_column)
        away_color = get_color(away_team, team_color_column, color_data_column)
        color_comparison = compare_color(home_color, away_color)
        if color_comparison[1] == color_comparison[2]:
            home_color = "black"
            away_color = "red"
        return {1: color_comparison[1], 2: color_comparison[2]}
    else:
        return "There was an error in contacting Google Sheets, please try again."


"""
Return the color for the team requested

"""   


def get_color(team, team_color_column, color_data_column):
    team_column = team_color_column
    color_column = color_data_column
    i = 0
    color = "black"
    for value in team_column:
        if team == value:
            color = color_column[i]
            break
        i = i + 1
    return color


"""
Compare team colors and if they're within a threshold, use black and red
"""


def compare_color(home_color, away_color):
    if home_color != "black" and home_color is not None:
        home_hex = home_color.split("#")[1]
    else:
        home_hex = "000000"
    if away_color != "black" and away_color is not None:
        away_hex = away_color.split("#")[1]
    else:
        away_hex = "000000"
    home_decimal = int(home_hex, 16) 
    away_decimal = int(away_hex, 16)
    # If difference is greater than 330000 they are far enough apart
    if abs(home_decimal-away_decimal) < 330000:
        home_color = "black"
        away_color = "red"
        return {1: home_color, 2: away_color}
    else:
        return {1: home_color, 2: away_color}