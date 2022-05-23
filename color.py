from sheets_functions import *
import json

"""
Handle the colors aspect of the bot

@author: apkick
"""

with open('fbs_color.json', 'r') as config_file:
    fbs_color_data = json.load(config_file)

with open('fcs_color.json', 'r') as config_file:
    fcs_color_data = json.load(config_file)


"""
Get the colors for both teams playing

"""


def get_team_colors(home_team, away_team):
    home_color = get_primary_color(home_team)
    away_color = get_primary_color(away_team)

    color_comparison = compare_color(home_color, away_color)

    # Try to get secondary colors
    if color_comparison[1] == "Black":
<<<<<<< HEAD
        home_color = get_primary_color(home_team)
        away_color = get_secondary_color(away_team)
        color_comparison = compare_color(home_color, away_color)
        if color_comparison[1] == "Black":
            home_color = get_secondary_color(home_team)
            away_color = get_primary_color(away_team)
            color_comparison = compare_color(home_color, away_color)
            if color_comparison[1] == "Black":
                home_color = get_secondary_color(home_team)
                away_color = get_secondary_color(away_team)
=======
        home_color = get_secondary_color(home_team)
        away_color = get_secondary_color(away_team)
        color_comparison = compare_color(home_color, away_color)
        if color_comparison[1] == "Black":
            home_color = get_primary_color(home_team)
            away_color = get_secondary_color(away_team)
            color_comparison = compare_color(home_color, away_color)
            if color_comparison[1] == "Black":
                home_color = get_secondary_color(home_team)
                away_color = get_primary_color(away_team)
>>>>>>> fc08d1834828820fa06a447399d078cce40334d7
                color_comparison = compare_color(home_color, away_color)
                if color_comparison[1] == "Black":
                    color_comparison[1] = "#000000"
                    color_comparison[2] = "#FF0000"

    return {1: color_comparison[1], 2: color_comparison[2]}


"""
Get the primary team color from the json

"""


def get_primary_color(team):
    if team in fbs_color_data["primary_colors"]:
        color = fbs_color_data["primary_colors"][team]
    elif team in fcs_color_data["primary_colors"]:
        color = fcs_color_data["primary_colors"][team]
    else:
        color = "black"
        print("Could not find color for " + team)
    return color


"""
Get the secondary team color from the json and

"""


def get_secondary_color(team):
    if team in fbs_color_data["secondary_colors"]:
        color = fbs_color_data["secondary_colors"][team]
    elif team in fcs_color_data["secondary_colors"]:
        color = fcs_color_data["secondary_colors"][team]
    else:
        color = "black"
        print("Could not find color for " + team)
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
    if abs(home_decimal-away_decimal) > 330000:
        return {1: home_color, 2: away_color}
    else:
        return {1: "Black", 2: "Red"}
