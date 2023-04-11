import csv
import math
from win_probability import *
from plot_graphs import *
from vegas_odds import *
from sheets_functions import *

"""
Iterate through Gist data and post plots for that data

@author: apkick
"""

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
Iterate through Gist data and post plots for that data for a game

"""


def iterate_through_game_gist(home_team, away_team, home_color, away_color):
    home_score = []
    away_score = []
    home_win_probability = []
    away_win_probability = []
    play_number = []
    play_count = 1
    overtime_flag = 0
    time_elapsed_between_plays = 0
    time_elapsed_on_play = 0

    home_elo = 0
    away_elo = 0
    elo_dictionary = get_elo_data()
    if elo_dictionary != "There was an error in contacting Google Sheets, please try again.":
        team_elo_column = elo_dictionary[1]
        elo_data_column = elo_dictionary[2]
        home_elo = get_elo(home_team, team_elo_column, elo_data_column)
        away_elo = get_elo(away_team, team_elo_column, elo_data_column)
    
    # Iterate through playlist file
    with open('data.txt', 'r+') as csvfile:
        counter = csv.reader(csvfile, delimiter= '|', lineterminator='\n')  
        row_count = sum(1 for row in counter)
        
    with open('data.txt', 'r+') as csvfile:
        reader = csv.reader(csvfile, delimiter= '|', lineterminator='\n') 
        i = 1
        for row in reader:
            if len(row) > 2:
                time_elapsed_between_plays = 0
                time_elapsed_on_play = 0

                home_score.append(int(row[0])) 
                away_score.append(int(row[1]))

                possession = row[5]
                if possession == "home":
                    offense_score = row[0]
                    defense_score = row[1]
                else:
                    offense_score = row[1]
                    defense_score = row[0]
                margin = int(offense_score) - int(defense_score)

                # Get seconds left in half and seconds left in game and current half
                quarter = row[2]
                clock = row[3]
                if quarter == "1":
                    seconds_left_game = 1680 - (420 - int(clock))
                    seconds_left_half = 840 - (420 - int(clock))
                    half = 1
                elif quarter == "2":
                    seconds_left_game = 1260 - (420 - int(clock))
                    seconds_left_half = 420 - (420 - int(clock))
                    half = 1
                elif quarter == "3":
                    seconds_left_game = 840 - (420 - int(clock))
                    seconds_left_half = 840 - (420 - int(clock))
                    half = 2
                elif quarter == "4":
                    seconds_left_game = 420 - (420 - int(clock))
                    seconds_left_half = 420 - (420 - int(clock))
                    half = 2
                else:
                    seconds_left_game = 0
                    seconds_left_half = 0
                    half = 2

                if int(quarter) <= 4 and row[16] != "" and row[16] != "None":
                    time_elapsed_on_play = int(row[16])
                if int(quarter) <= 4 and row[17] != "" and row[17] != "None":
                    time_elapsed_between_plays = int(row[17])

                position = 100 - int(row[4])
                down = int(row[6])
                distance = int(row[7])

                # Get elo
                if possession == "home":
                    offense_elo = home_elo
                    defense_elo = away_elo
                else:
                    offense_elo = away_elo
                    defense_elo = home_elo

                elo_diff_time = (float(offense_elo) - float(defense_elo)) * math.exp(-2 * (1 - (seconds_left_game / 1680)))

                play_number.append(int(play_count))
                play_count = play_count + 1
                
                # Set all the data in the dictionary
                # If the home team has the ball on line 1, it means they kicked it off and deferred
                if i == 1 and possession == "home":
                    had_first_possession = 0
                elif i == 1 and possession == "away":
                    had_first_possession = 1

                play_type = row[12]

                # Calculate win probability
                cur_win_probability = abs(get_win_probability(down, distance, position, margin, seconds_left_game,
                                                          seconds_left_half, half, had_first_possession,
                                                          elo_diff_time, play_type))
                if row[5] == "home" and "KICKOFF" not in row[12] and row[12] != "PAT" and row[12] != "TWO POINT":
                    home_win_probability.append(cur_win_probability)
                    away_win_probability.append(100 - cur_win_probability)
                elif row[5] == "home" and ("KICKOFF" in row[12] or row[12] != "PAT" or row[12] != "TWO POINT"):
                    home_win_probability.append(100 - cur_win_probability)
                    away_win_probability.append(cur_win_probability)
                elif row[5] == "away" and "KICKOFF" not in row[12] and row[12] != "PAT" and row[12] != "TWO POINT":
                    home_win_probability.append(100 - cur_win_probability)
                    away_win_probability.append(cur_win_probability)
                elif row[5] == "away" and ("KICKOFF" in row[12] or row[12] != "PAT" or row[12] != "TWO POINT"):
                    home_win_probability.append(cur_win_probability)
                    away_win_probability.append(100 - cur_win_probability)
                    
                if int(quarter) > 4:
                    overtime_flag = 1

            i = i + 1

    if time_elapsed_on_play is None:
        time_elapsed_on_play = 0
    if time_elapsed_between_plays is None:
        time_elapsed_between_plays = 0
    
    # Plot score plot
    plot_score_gist(home_team, away_team, home_score, away_score, play_number, home_color, away_color, overtime_flag)
   
    # Plot win probability
    plot_win_probability_gist(home_team, away_team, home_win_probability, away_win_probability, play_number, home_color,
                              away_color)
