import math
import csv
import xgboost as xgb
import pandas as pd
import m2cgen as m2c
from vegas_odds import *
from sheets_functions import *
from scipy.stats import norm

"""
Calculate the win probability for various scenarios

@author: apkick
"""

model_xgb = xgb.XGBRegressor()
model_xgb.load_model('wpmodel.json')

data = {
  'down': [4],
  'distance': [4],
  'position': [38],
  'margin': [17],
  'seconds_left_game': [350],
  'seconds_left_half': [350],
  'half': [2],
  'had_first_possession': [1],
  'elo_diff_time': [27.0449]
}

"""
Get the current win probability for the current play for an ongoing game

"""
def get_in_game_win_probability(home_team, away_team):
    win_probability_list = []

    home_elo = 0
    away_elo = 0
    elo_dictionary = getEloData()
    if elo_dictionary != "There was an error in contacting Google Sheets, please try again.":
        team_elo_column = elo_dictionary[1]
        elo_data_column = elo_dictionary[2]
        home_elo = get_elo(home_team, team_elo_column, elo_data_column)
        away_elo = get_elo(away_team, team_elo_column, elo_data_column)
    
    #Iterate through playlist file
    with open('data.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n')
        i = 0
        for row in reader:
            if (len(row) > 2):
                # Get margin in score
                offense_score = "0"
                defense_score = "0"
                possession = row[5]
                if possession == "home":
                    offense_score = row[0]
                    defense_score = row[1]
                else:
                    offense_score = row[1]
                    defense_score = row[0]
                margin = int(offense_score) - int(defense_score)

                # Get seconds left in half and seconds left in game and current half
                seconds_left_game = 1680
                seconds_left_half = 840
                half = 0
                quarter = row[2]
                clock = row[3]
                if quarter == "1":
                    seconds_left_game = 1680-(420-int(clock))
                    seconds_left_half = 840-(420-int(clock))
                    half = 1
                elif quarter == "2":
                    seconds_left_game = 1260-(420-int(clock))
                    seconds_left_half = 420-(420-int(clock))
                    half = 1
                elif quarter == "3":
                    seconds_left_game = 840-(420-int(clock))
                    seconds_left_half = 840-(420-int(clock))
                    half = 2
                elif quarter == "4":
                    seconds_left_game = 420-(420-int(clock))
                    seconds_left_half = 420-(420-int(clock))
                    half = 2
                else:
                    seconds_left_game = 0
                    seconds_left_half = 0
                    half = 2

                position = 100-int(row[4])
                down = int(row[6])
                distance = int(row[7])

                # Get elo
                offense_elo = 0
                defense_elo = 0
                elo_diff_time = 0
                if possession == "home":
                    offense_elo = home_elo
                    defense_elo = away_elo
                else:
                    offense_elo = away_elo
                    defense_elo = home_elo

                elo_diff_time = (float(offense_elo) - float(defense_elo)) * math.exp(-2 * (1 - (seconds_left_game / 1680)))

                # Set all the data in the dictionary
                # If the home team has the ball on line 1, it means they kicked it off and deferred
                if i == 1 and possession == "home":
                      data["had_first_possession"] = [0]
                elif i == 1 and possession == "away":
                      data["had_first_possession"] = [1]
                data["margin"] = [margin]
                data["down"] = [down]
                data["distance"] = [distance]
                data["position"] = [position]
                data["seconds_left_game"] = [seconds_left_game]
                data["seconds_left_half"] = [seconds_left_half]
                data["half"] = [half]
                data["elo_diff_time"] = [elo_diff_time]

                current_win_probability = calculate_win_probability_gist(data)
                win_probability_list.append(current_win_probability)

                i += 1
                    
        return win_probability_list[-1]
    
"""
Calculate the win probability for the thread crawler

"""                     
def calculate_win_probability_thread_crawler(expected_points, quarter, time, team_score, opponent_score, down, distance, yard_line, play_type, vegas_line):
    if(time == 0):
        time = 0.00001
    minutes_in_quarter = time/60
    minutes_remaining = 28
    if(quarter == 1):
        minutes_remaining = 28-(7-minutes_in_quarter)
    elif(quarter == 2):
        minutes_remaining = 21-(7-minutes_in_quarter)
    elif(quarter == 3):
        minutes_remaining = 14-(7-minutes_in_quarter)
    elif(quarter == 4):
        minutes_remaining = 7-(7-minutes_in_quarter)
    else:
        minutes_remaining = 2
    
    if(minutes_remaining < 0):
        minutes_remaining = 0.01
        
    opponent_margin = opponent_score - team_score
    opponent_margin = opponent_margin - expected_points
        
    stdDev = (13.45/math.sqrt((28/minutes_remaining)))
        
    win_probability = ((1-norm.cdf(((opponent_margin)+0.5),(-vegas_line*(minutes_remaining/28)),stdDev))
    +(0.5*(norm.cdf(((opponent_margin)+0.5), (-vegas_line*(minutes_remaining/28)), stdDev)
    - norm.cdf(((opponent_margin)-0.5),(-vegas_line*(minutes_remaining/28)), stdDev))))
    
    return win_probability

"""
Calculate the win probability for the Gist data

""" 
def calculate_win_probability_gist(data):
    dfData = pd.DataFrame.from_dict(data)
    win_probability = model_xgb.predict(dfData)

    return float(win_probability)*100
    
"""
Calculate the expected points, used to tell the formula information so it can calculate
based on current scenarios

""" 
def calculate_expected_points(down, distance, yard_line, play_type):
    if ((play_type == 'PAT') or (play_type == 'TWO_POINT')):
        return 0.952
        
    if ("KICKOFF" in play_type):
        return 0 - calculate_expected_points(1, 10, 25, "EMPTY")
    
    intercept = 0
    slope = 0
    avgDist = 0
    distanceDiff = 0
    
    if(down == 1):
        avgDist = 10
        intercept = 2.43
        slope = 0.0478
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
    elif(down == 2):
        avgDist = 7.771
        intercept = 2.07
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
        slope = (distanceDiff * 0.0015) + 0.055
    elif(down == 3):
        avgDist = 6.902
        intercept = 1.38
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
        slope = (distanceDiff * 0.0015) + 0.055
    elif(down == 4):
        avgDist = 6.864
        intercept = -0.03
        distanceDiff = distance - avgDist
        intercept = (distanceDiff / -10) + intercept
        slope = (distanceDiff * 0.0015) + 0.055
    
    if(down == 1):
        return intercept + (slope * (yard_line - 50)) + (((yard_line - 50) ** 3) / 100000) + max(0, (((1.65 ** 0.2) ** (yard_line - 94)) - 1) * (4))
    return intercept + (slope * (yard_line - 50)) + (((yard_line - 50) ** 3) / 100000) + max(0, (((1.65 ** 0.2) ** (yard_line - 94)) - 1) * (down/4))
