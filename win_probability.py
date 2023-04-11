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
    elo_dictionary = get_elo_data()
    if elo_dictionary != "There was an error in contacting Google Sheets, please try again.":
        team_elo_column = elo_dictionary[1]
        elo_data_column = elo_dictionary[2]
        home_elo = get_elo(home_team, team_elo_column, elo_data_column)
        away_elo = get_elo(away_team, team_elo_column, elo_data_column)
    
    # Iterate through playlist file
    with open('data.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|', lineterminator='\n')
        i = 0
        last_play_possession_change = False
        play = None
        result = None
        for row in reader:
            if len(row) > 2:
                # Get margin in score
                possession = row[5]
                if possession == "home":
                    offense_score = row[0]
                    defense_score = row[1]
                elif possession == "away":
                    offense_score = row[1]
                    defense_score = row[0]
                elif possession == "home" and str(result) == "TOUCHDOWN":
                    offense_score = str(int(row[0]) + 6)
                    defense_score = row[1]
                elif possession == "away" and str(result) == "TOUCHDOWN":
                    offense_score = str(int(row[1]) + 6)
                    defense_score = row[0]
                elif possession == "home" and str(result) == "TURNOVER_TOUCHDOWN":
                    offense_score = str(int(row[1]) + 6)
                    defense_score = row[0]
                elif possession == "away" and str(result) == "TURNOVER_TOUCHDOWN":
                    offense_score = str(int(row[0]) + 6)
                    defense_score = row[1]
                elif possession == "home" and str(result) == "PAT":
                    offense_score = str(int(row[0]) + 1)
                    defense_score = row[1]
                elif possession == "away" and str(result) == "PAT":
                    offense_score = str(int(row[1]) + 1)
                    defense_score = row[0]
                elif possession == "home" and str(result) == "TWO_POINT":
                    offense_score = str(int(row[0]) + 2)
                    defense_score = row[1]
                elif possession == "away" and str(result) == "TWO_POINT":
                    offense_score = str(int(row[1]) + 2)
                    defense_score = row[0]
                margin = int(offense_score) - int(defense_score)

                # Get seconds left in half and seconds left in game and current half
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

                if str(play) == "PAT" or str(play) == "TWO_POINT" or str(result) == "TURNOVER" or "KICKOFF" in str(play):
                    last_play_possession_change = True
                else:
                    last_play_possession_change = False

                play = row[12]
                result = row[14]

                # Get elo
                if possession == "home":
                    offense_elo = home_elo
                    defense_elo = away_elo
                else:
                    offense_elo = away_elo
                    defense_elo = home_elo

                elo_diff_time = (float(offense_elo) - float(defense_elo)) * math.exp(-2 * (1 - (seconds_left_game / 1680)))

                if i == 1 and possession == "home":
                    had_first_possession = 0
                elif i == 1 and possession == "away":
                    had_first_possession = 1

                current_win_probability = get_win_probability(down, distance, position, margin, seconds_left_game,
                                                              seconds_left_half, half, had_first_possession,
                                                              elo_diff_time, str(play))
                win_probability_list.append(current_win_probability)

                i += 1

        return {1: win_probability_list[-1], 2: last_play_possession_change}


def get_win_probability(down, distance, position, margin, seconds_left_game, seconds_left_half, half,
                        had_first_possession, elo_diff_time, play_type):
    """
    Get the win probability for the play

    :param down:
    :param distance:
    :param position:
    :param margin:
    :param seconds_left_game:
    :param seconds_left_half:
    :param half:
    :param had_first_possession:
    :param elo_diff_time:
    :param play_type:
    :return:
    """

    if seconds_left_game == 0 and play_type != "PAT":
        return 1 if margin > 0 else (0 if margin < 0 else 0.5)

    if play_type == "PAT":
        prob_if_success = get_win_probability(1, 10, 75, -(margin + 1), seconds_left_game, seconds_left_half, half,
                                              1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_fail = get_win_probability(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                           1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_return = get_win_probability(1, 10, 75, -(margin - 2), seconds_left_game, seconds_left_half, half,
                                             1-had_first_possession, -elo_diff_time, 'RUN')
        return 1 - (((721 / 751) * prob_if_success) + ((27 / 751) * prob_if_fail) + ((3 / 751) * prob_if_return))
    if play_type == 'TWO_POINT':
        prob_if_success = get_win_probability(1, 10, 75, -(margin + 2), seconds_left_game, seconds_left_half, half,
                                              1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_fail = get_win_probability(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                           1-had_first_possession, -elo_diff_time, 'RUN')
        prob_if_return = get_win_probability(1, 10, 75, -(margin - 2), seconds_left_game, seconds_left_half, half,
                                             1-had_first_possession, -elo_diff_time, 'RUN')
        return 1 - (((301 / 751) * prob_if_success) + ((447  / 751) * prob_if_fail) + ((3 / 751) * prob_if_return))
    if play_type == 'KICKOFF_NORMAL':
        return 1 - get_win_probability(1, 10, 75, -margin, seconds_left_game, seconds_left_half, half,
                                       1-had_first_possession, -elo_diff_time, 'RUN')
    if play_type == 'KICKOFF_SQUIB':
        slh = max(seconds_left_half - 5, 0)
        slg = ((2 - half) * 840) + slh
        return 1 - get_win_probability(1, 10, 65, -margin, slg, slh, half, 1-had_first_possession, -elo_diff_time,
                                       'RUN')
    if play_type == 'KICKOFF_ONSIDE':
        slh = max(seconds_left_half - 3, 0)
        slg = ((2 - half) * 840) + slh
        prob_if_success = get_win_probability(1, 10, 55, margin, slg, slh, half, 1-had_first_possession, elo_diff_time,
                                              'RUN')
        prob_if_fail = 1-get_win_probability(1, 10, 45, -margin, slg, slh, half, 1-had_first_possession, -elo_diff_time,
                                             'RUN')
        slhr = max(seconds_left_half - 10, 0)
        slgr = ((2 - half) * 840) + slh
        prob_if_return = 1-get_win_probability(1, 10, 75, margin - 6, slgr, slhr, half, 1-had_first_possession,
                                               -elo_diff_time, 'PAT')
        return ((140 / 751) * prob_if_success) + ((611 / 751) * prob_if_fail) + ((1 / 751) * prob_if_return)

    data["had_first_possession"] = [had_first_possession]
    data["margin"] = [margin]
    data["down"] = [down]
    data["distance"] = [distance]
    data["position"] = [position]
    data["seconds_left_game"] = [seconds_left_game]
    data["seconds_left_half"] = [seconds_left_half]
    data["half"] = [half]
    data["elo_diff_time"] = [elo_diff_time]

    return calculate_win_probability_gist(data)

    
"""
Calculate the win probability for the thread crawler

""" 


def calculate_win_probability_thread_crawler(expected_points, quarter, time, team_score, opponent_score, down, distance, yard_line, play_type, vegas_line):
    if time == 0:
        time = 0.00001
    minutes_in_quarter = time/60
    minutes_remaining = 28
    if quarter == 1:
        minutes_remaining = 28-(7-minutes_in_quarter)
    elif quarter == 2:
        minutes_remaining = 21-(7-minutes_in_quarter)
    elif quarter == 3:
        minutes_remaining = 14-(7-minutes_in_quarter)
    elif quarter == 4:
        minutes_remaining = 7-(7-minutes_in_quarter)
    else:
        minutes_remaining = 2
    
    if minutes_remaining < 0:
        minutes_remaining = 0.01
        
    opponent_margin = opponent_score - team_score
    opponent_margin = opponent_margin - expected_points
        
    stdDev = (13.45/math.sqrt((28/minutes_remaining)))
        
    win_probability = ((1 - norm.cdf((opponent_margin + 0.5), (-vegas_line * (minutes_remaining / 28)), stdDev))
                       + (0.5 * (norm.cdf((opponent_margin + 0.5), (-vegas_line * (minutes_remaining / 28)), stdDev)
                                - norm.cdf((opponent_margin - 0.5), (-vegas_line * (minutes_remaining / 28)), stdDev))))
    
    return win_probability


"""
Calculate the win probability for the Gist data

""" 


def calculate_win_probability_gist(data):
    df_data = pd.DataFrame.from_dict(data)
    win_probability = model_xgb.predict(df_data)

    return float(win_probability)*100
    
    
"""
Calculate the expected points, used to tell the formula information so it can calculate
based on current scenarios

""" 


def calculate_expected_points(down, distance, yard_line, play_type):
    if play_type == 'PAT' or play_type == 'TWO_POINT':
        return 0.952
        
    if "KICKOFF" in play_type:
        return 0 - calculate_expected_points(1, 10, 25, "EMPTY")
    
    intercept = 0
    slope = 0
    
    if down == 1:
        avg_dist = 10
        intercept = 2.43
        slope = 0.0478
        distance_diff = distance - avg_dist
        intercept = (distance_diff / -10) + intercept
    elif down == 2:
        avg_dist = 7.771
        intercept = 2.07
        distance_diff = distance - avg_dist
        intercept = (distance_diff / -10) + intercept
        slope = (distance_diff * 0.0015) + 0.055
    elif down == 3:
        avg_dist = 6.902
        intercept = 1.38
        distance_diff = distance - avg_dist
        intercept = (distance_diff / -10) + intercept
        slope = (distance_diff * 0.0015) + 0.055
    elif down == 4:
        avg_dist = 6.864
        intercept = -0.03
        distance_diff = distance - avg_dist
        intercept = (distance_diff / -10) + intercept
        slope = (distance_diff * 0.0015) + 0.055
    
    if down == 1:
        return intercept + (slope * (yard_line - 50)) + (((yard_line - 50) ** 3) / 100000) + max(0, (((1.65 ** 0.2) ** (yard_line - 94)) - 1) * (4))
    return intercept + (slope * (yard_line - 50)) + (((yard_line - 50) ** 3) / 100000) + max(0, (((1.65 ** 0.2) ** (yard_line - 94)) - 1) * (down/4))
