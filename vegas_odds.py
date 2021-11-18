from sheets_functions import *

"""
Handle calculating vegas odds for games

@author: apkick
"""


"""
Get the team Elo for the team requested

"""


def get_elo(team, team_elo_column, elo_data_column):
    team_column = team_elo_column
    elo_column = elo_data_column
    elo = 0
    i = 0
    for value in team_column:
        if "(" in value:
            value = value.split("(")[0]
            value = value.strip()
        if team == value:
            elo = elo_column[i]
            break
        i = i + 1
    if elo == 0:
        return -500
    return elo


"""
Calculate Vegas odds using a constant and team and their opponent Elo

"""


def calculate_vegas_odds(team_elo, opponent_elo):
    constant = 18.14010981807
    odds = (float(opponent_elo) - float(team_elo))/constant
    return odds


"""
Return a dictionary containing the Vegas Odds for the game

"""


def get_vegas_odds(home_team, away_team):
    elo_dictionary = get_elo_data()
    if elo_dictionary != "There was an error in contacting Google Sheets, please try again.":
        team_elo_column = elo_dictionary[1]
        elo_data_column = elo_dictionary[2]
        home_elo = get_elo(home_team, team_elo_column, elo_data_column)
        away_elo = get_elo(away_team, team_elo_column, elo_data_column)
        home_odds = calculate_vegas_odds(home_elo, away_elo)
        away_odds = calculate_vegas_odds(away_elo, home_elo)
        # Default to a push if can't find Elo
        if home_elo == -500 or away_elo == -500:
            home_odds = 0
            away_odds = 0
        return{1: home_odds, 2: away_odds}
    else:
        return elo_dictionary
    
    

