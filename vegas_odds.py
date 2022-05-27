from database_functions import *

"""
Handle calculating vegas odds for games

@author: apkick
"""

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


def get_vegas_odds(home_team, away_team, database):
    home_elo = get_elo(database, home_team)
    away_elo = get_elo(database, away_team)
    if home_elo == None or away_elo == None:
        return None

    home_odds = calculate_vegas_odds(home_elo, away_elo)
    away_odds = calculate_vegas_odds(away_elo, home_elo)
    # Default to a push if can't find Elo
    if home_elo == -500 or away_elo == -500:
        home_odds = 0
        away_odds = 0
    return{1: home_odds, 2: away_odds}
    
    

