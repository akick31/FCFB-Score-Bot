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
    with open('/home/ubuntu/FCFB/FCFB-Score-Bot/data.txt', 'r+') as csvfile:
        counter = csv.reader(csvfile, delimiter= '|', lineterminator='\n')  
        row_count = sum(1 for row in counter)
        
    with open('/home/ubuntu/FCFB/FCFB-Score-Bot/data.txt', 'r+') as csvfile:
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

                if possession == "home":
                    cur_home_win_probability = calculate_win_probability_gist(data)
                    cur_away_win_probability = abs(100-cur_home_win_probability)
                    home_win_probability.append(cur_home_win_probability)
                    away_win_probability.append(cur_away_win_probability)
                elif possession == "away":
                    cur_away_win_probability = calculate_win_probability_gist(data)
                    cur_home_win_probability = abs(100 - cur_away_win_probability)
                    home_win_probability.append(cur_home_win_probability)
                    away_win_probability.append(cur_away_win_probability)
                    
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
    plot_win_probability_gist(home_team, away_team, home_win_probability, away_win_probability, play_number, home_color, away_color)
