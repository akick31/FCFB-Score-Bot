from win_probability import *
from plot_graphs import *

"""
Crawl through an old Game Thread (pre-Season 4) and gather game data and plot it

@author: apkick
"""


"""
Crawl through old season threads and plot the win probability and score

"""


def thread_crawler(home_team, away_team, home_vegas_odds, away_vegas_odds, home_color, away_color, season, submission):
    submission.comment_sort = "old"

    if home_team.find('-') >= 0:
        home_team = home_team.replace('-', '–')
    if away_team.find('-') >= 0:
        away_team = away_team.replace('-', '–')
    
    if home_team == "Massachusetts":
        home_team = "UMass"
    elif away_team == "Massachusetts":
        away_team = "UMass"
    
    home_user = ""
    away_user = ""
    home_score = 0
    away_score = 0
    ot_flag = 0
    quarter = 1
    clock = "7:00"
    yard_line = 25
    possession = "home"
    down = 1
    distance = 10
    play_type = "EMPTY"
    cur_data = ""
    home_score_list = []
    away_score_list = []
    home_win_probability = []
    away_win_probability = []
    play_number = []
    play_count = 1
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        if ot_flag == 1:
            break
        if comment.author == 'NFCAAOfficialRefBot' and 'you\'re home' in comment.body:
            home_user = comment.body.split("The game has started!")[1].split(",")[0].strip()
            away_user = comment.body.split("The game has started!")[1].split(",")[1].split("home. ")[1].strip()
        # Handle delay of game
        if comment.author == 'NFCAAOfficialRefBot' and 'not sent their number in over 24 hours' in comment.body and "touchdown" in comment.body:
            if home_user in comment.body:
                away_score = away_score + 8
                play_type = "PAT"
                   
                home_score_list.append(home_score)
                away_score_list.append(away_score)
                play_number.append(int(play_count))
                play_count = play_count + 1
                                
                m, s = clock.split(':')
                game_time = int(m) * 60 + int(s)
                                
                expected_points = calculate_expected_points(int(down), int(distance), int(yard_line), play_type)
                if possession == "home":
                    cur_home_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, home_score, away_score, int(down), int(distance), int(yard_line), play_type, home_vegas_odds) * 100
                    cur_away_win_probability = 100 - cur_home_win_probability
                    home_win_probability.append(cur_home_win_probability)
                    away_win_probability.append(cur_away_win_probability)
                elif possession == "away":
                    cur_away_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, away_score, home_score, int(down), int(distance), int(yard_line), play_type, away_vegas_odds) * 100
                    cur_home_win_probability = 100 - cur_away_win_probability
                    away_win_probability.append(cur_away_win_probability)
                    home_win_probability.append(cur_home_win_probability) 
                cur_data = (str(home_score) + " | " + str(away_score) + " | " + str(quarter) + " | " + clock + " | "
                                  + str(yard_line) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + play_type)
                
            if away_user in comment.body:
                home_score = home_score + 8
                play_type = "PAT"
               
                home_score_list.append(home_score)
                away_score_list.append(away_score)
                play_number.append(int(play_count))
                play_count = play_count + 1
                            
                m, s = clock.split(':')
                game_time = int(m) * 60 + int(s)
                            
                expected_points = calculate_expected_points(int(down), int(distance), int(yard_line), play_type)
                if possession == "home":
                    cur_home_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, home_score, away_score, int(down), int(distance), int(yard_line), play_type, home_vegas_odds) * 100
                    cur_away_win_probability = 100 - cur_home_win_probability
                    home_win_probability.append(cur_home_win_probability)
                    away_win_probability.append(cur_away_win_probability)
                elif possession == "away":
                    cur_away_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, away_score, home_score, int(down), int(distance), int(yard_line), play_type, away_vegas_odds) * 100
                    cur_home_win_probability = 100 - cur_away_win_probability
                    away_win_probability.append(cur_away_win_probability)
                    home_win_probability.append(cur_home_win_probability)
                cur_data = (str(home_score) + " | " + str(away_score) + " | " + str(quarter) + " | " + clock + " | "
                                  + str(yard_line) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + play_type)
                
        if comment.author == 'NFCAAOfficialRefBot' and 'not sent their number in over 24 hours' in comment.body and "touchdown" in comment.body:
            if home_user in comment.body:
                away_score = away_score
                   
                home_score_list.append(home_score)
                away_score_list.append(away_score)
                play_number.append(int(play_count))
                play_count = play_count + 1
                                
                m, s = clock.split(':')
                game_time = int(m) * 60 + int(s)
                                
                expected_points = calculate_expected_points(int(down), int(distance), int(yard_line), play_type)
                if possession == "home":
                    cur_home_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, away_score, home_score, int(down), int(distance), int(yard_line), play_type, home_vegas_odds) * 100
                    cur_away_win_probability = 100 - cur_home_win_probability
                    home_win_probability.append(cur_home_win_probability)
                    away_win_probability.append(cur_away_win_probability)
                elif possession == "away":
                    cur_away_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, home_score, away_score, int(down), int(distance), int(yard_line), play_type, away_vegas_odds) * 100
                    cur_home_win_probability = 100 - cur_away_win_probability
                    away_win_probability.append(cur_away_win_probability)
                    home_win_probability.append(cur_home_win_probability) 
                cur_data = (str(home_score) + " | " + str(away_score) + " | " + str(quarter) + " | " + clock + " | "
                                  + str(yard_line) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + play_type)
                
            if away_user in comment.body:
                home_score = home_score
               
                home_score_list.append(home_score)
                away_score_list.append(away_score)
                play_number.append(int(play_count))
                play_count = play_count + 1
                            
                m, s = clock.split(':')
                timegame_time = int(m) * 60 + int(s)

                expected_points = calculate_expected_points(int(down), int(distance), int(yard_line), play_type)
                if possession == "home":
                    cur_home_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, home_score, away_score, int(down), int(distance), int(yard_line), play_type, home_vegas_odds) * 100
                    cur_away_win_probability = 100 - cur_home_win_probability
                    home_win_probability.append(cur_home_win_probability)
                    away_win_probability.append(cur_away_win_probability)
                elif possession == "away":
                    cur_away_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, away_score, home_score, int(down), int(distance), int(yard_line), play_type, away_vegas_odds) * 100
                    cur_home_win_probability = 100 - cur_away_win_probability
                    away_win_probability.append(cur_away_win_probability)
                    home_win_probability.append(cur_home_win_probability)
                cur_data = (str(home_score) + " | " + str(away_score) + " | " + str(quarter) + " | " + clock + " | "
                                  + str(yard_line) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + play_type)
                   
        # Look through top level comment
        if comment.author == 'NFCAAOfficialRefBot' and 'has submitted their' in comment.body and ot_flag != 1:
            if ot_flag == 1:
                break
            # Get the clock and quarter
            clock = comment.body.split("left in the")[0].split("on the")[-1].split(". ")[-1]
            quarter = comment.body.split("left in the ")[1].split(".")[0]
            if quarter == "1st":
                quarter = 1
            elif quarter == "2nd":
                quarter = 2
            elif quarter == "3rd":
                quarter = 3
            elif quarter == "4th":
                quarter = 4
            
            # Handle non kickoff and PATs
            if "kicking off" not in comment.body and "PAT" not in comment.body:
                # Get the down and distance
                down = comment.body.split("It\'s ")[-1].split(" and")[0]
                distance = comment.body.split("It\'s ")[-1].split(" and ")[1].split("on the")[0].strip()
                if down == "1st":
                    down = 1
                elif down == "2nd":
                    down = 2
                elif down == "3rd":
                    down = 3
                elif down == "4th":
                    down = 4
                    
                # Get the current possession
                possession_user = comment.body.split(" reply ")[0].split("\n")[-1]
                if possession_user == home_user:
                    possession = "home"
                elif possession_user == away_user:
                    possession = "away"
                
                # Get the current yard line
                if "50" not in comment.body.split(" on the ")[1].split(".")[0].split(" "):
                    yard_line = comment.body.split(" on the ")[1].split(".")[0].split(" ")[-1]
                    side_of_field = ""
                    for item in comment.body.split(" on the ")[1].split(".")[0].split(" ")[:-1]:
                        side_of_field = side_of_field + " " + item
                    side_of_field = side_of_field.strip()
                    if possession == "home" and side_of_field == away_team:
                        yard_line = 100-int(yard_line)
                    elif possession == "away" and side_of_field == home_team:
                        yard_line = 100-int(yard_line)
                else:
                    yard_line = 50
                
                # Handle "and goal" situations
                if distance == "goal":
                    distance = 100-int(yard_line)             
            else:
                down = 1
                distance = 10
            if "kicking off" in comment.body:
                yard_line = 35
                possession_user = comment.body.split(" reply ")[0].split("\n")[-1]
                if possession_user == home_user:
                    possession = "home"
                elif possession_user == away_user:
                    possession = "away"
                
            if "PAT" in comment.body:
                yard_line = 97
                possession_user = comment.body.split(" reply ")[0].split("\n")[-1]
                if possession_user == home_user:
                    possession = "home"
                elif possession_user == away_user:
                    possession = "away"
            for secondLevelComment in comment.replies:
                if ot_flag == 1:
                    break
                # Look through second level comment  
                if " and " in home_user:
                    home_user1 = home_user.split(" and ")[0]
                    home_user2 = home_user.split(" and ")[1]
                else:
                    home_user1 = home_user
                    home_user2 = "BLANK USER"
                if " and " in away_user:
                    away_user1 = away_user.split(" and ")[0]
                    away_user2 = away_user.split(" and ")[1]
                else:
                    away_user1 = away_user
                    away_user2 = "BLANK USER"
                if (secondLevelComment.author == home_user1.split("/u/")[-1] or secondLevelComment.author == away_user1.split("/u/")[-1]
                   or secondLevelComment.author == home_user2.split("/u/")[-1] or secondLevelComment.author == away_user2.split("/u/")[-1]):
                    comment_list = secondLevelComment.body.split(" ")
                    if ot_flag == 1:
                        break
                    comment_list = [x.lower() for x in comment_list]
                    if "normal" in comment_list:
                        play_type = "KICKOFF_NORMAL"
                    elif "squib" in comment_list:
                        play_type = "KICKOFF_SQUIB"
                    elif "onside" in comment_list:
                        play_type = "KICKOFF_ONSIDE"  
                    elif "pat" in comment_list:
                        play_type = "PAT"
                    elif "two" in comment_list and "point" in comment_list:
                        play_type = "TWO_POINT"
                    else:
                        play_type = "EMPTY"
                    for third_level_comment in secondLevelComment.replies:
                        if season != "S1":
                            # Look through third level comments
                            if (third_level_comment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in third_level_comment.body
                                  and away_user in third_level_comment.body):
                                home_score = home_score + 1
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in third_level_comment.body
                                  and home_user in third_level_comment.body):
                                away_score = away_score + 1
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and ('The two point was successful' in third_level_comment.body
                                  or 'The two point conversion is successful' in third_level_comment.body
                                  and away_user in third_level_comment.body)):
                                home_score = home_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and ('The two point was successful' in third_level_comment.body
                                  or 'The two point conversion is successful' in third_level_comment.body
                                  and home_user in third_level_comment.body)):
                                away_score = away_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'safety' in third_level_comment.body
                                  and away_user in third_level_comment.body):
                                away_score = away_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'safety' in third_level_comment.body
                                  and home_user in third_level_comment.body):
                                home_score = home_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in third_level_comment.body
                                  and away_user in third_level_comment.body):
                                home_score = home_score + 3
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in third_level_comment.body
                                  and home_user in third_level_comment.body):
                                away_score = away_score + 3
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'just scored' in third_level_comment.body 
                                  and 'PAT or two point' not in third_level_comment.body and away_user in third_level_comment.body):
                                home_score = home_score + 6
                                play_type = "PAT"
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'just scored' in third_level_comment.body
                                  and 'PAT or two point' not in third_level_comment.body and home_user in third_level_comment.body):
                                away_score = away_score + 6
                                play_type = "PAT"
                        elif season == "S1":
                            # Look through third level comments
                            if (third_level_comment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in third_level_comment.body
                                  and home_team + " is kicking off"  in third_level_comment.body):
                                home_score = home_score + 1
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in third_level_comment.body
                                  and away_team + " is kicking off" in third_level_comment.body):
                                away_score = away_score + 1
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and ('The two point was successful' in third_level_comment.body
                                  or 'The two point conversion is successful' in third_level_comment.body)
                                  and home_team + " is kicking off" in third_level_comment.body):
                                home_score = home_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and ('The two point was successful' in third_level_comment.body
                                  or 'The two point conversion is successful' in third_level_comment.body)
                                  and away_team + " is kicking off" in third_level_comment.body):
                                away_score = away_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'safety' in third_level_comment.body
                                  and away_team + " is kicking off" in third_level_comment.body):
                                away_score = away_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'safety' in third_level_comment.body
                                  and home_team + " is kicking off" in third_level_comment.body):
                                home_score = home_score + 2
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in third_level_comment.body
                                  and home_team + " is kicking off" in third_level_comment.body):
                                home_score = home_score + 3
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in third_level_comment.body
                                  and away_team + " is kicking off" in third_level_comment.body):
                                away_score = away_score + 3
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'just scored' in third_level_comment.body 
                                  and home_team + " just scored." in third_level_comment.body):
                                home_score = home_score + 6
                                play_type = "PAT"
                            elif (third_level_comment.author == 'NFCAAOfficialRefBot' and 'just scored' in third_level_comment.body
                                  and away_team + " just scored." in third_level_comment.body):
                                away_score = away_score + 6
                                play_type = "PAT"
                        if third_level_comment.author == 'NFCAAOfficialRefBot' and "we're going to overtime!" in third_level_comment.body:
                            ot_flag = 0
                            break
                        # Add data
                        if third_level_comment.author == 'NFCAAOfficialRefBot' and "I'm not waiting on a message from you" not in third_level_comment.body:
                            # Fill plot data
                            cur_data = (str(home_score) + " | " + str(away_score) + " | " + str(quarter) + " | " + clock + " | "
                                  + str(yard_line) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + play_type)
                            home_score_list.append(home_score)
                            away_score_list.append(away_score)
                            play_number.append(int(play_count))
                            play_count = play_count + 1
                            
                            m, s = clock.split(':')
                            game_time = int(m) * 60 + int(s)
                            if game_time == 0 and int(quarter) == 4:
                                if home_score > away_score:
                                    cur_home_win_probability = 100
                                    cur_away_win_probability = 100 - cur_home_win_probability
                                    home_win_probability.append(cur_home_win_probability)
                                    away_win_probability.append(cur_away_win_probability)
                                elif home_score < away_score:
                                    cur_away_win_probability = 100
                                    cur_home_win_probability = 100 - cur_away_win_probability
                                    away_win_probability.append(cur_away_win_probability)
                                    home_win_probability.append(cur_home_win_probability)
                                break
                            expected_points = calculate_expected_points(int(down), int(distance), int(yard_line), play_type)
                            if possession == "home":
                                cur_home_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, home_score, away_score, int(down), int(distance), int(yard_line), play_type, home_vegas_odds) * 100
                                cur_away_win_probability = 100 - cur_home_win_probability
                                home_win_probability.append(cur_home_win_probability)
                                away_win_probability.append(cur_away_win_probability)
                            elif possession == "away":
                                cur_away_win_probability = calculate_win_probability_thread_crawler(expected_points, int(quarter), game_time, away_score, home_score, int(down), int(distance), int(yard_line), play_type, away_vegas_odds) * 100
                                cur_home_win_probability = 100 - cur_away_win_probability
                                away_win_probability.append(cur_away_win_probability)
                                home_win_probability.append(cur_home_win_probability) 
                            
                        # If end of game, make sure WP is 100% and 0%
                        if third_level_comment.author == 'NFCAAOfficialRefBot' and "that's the end of the game" in third_level_comment.body:
                            home_score_list.append(home_score)
                            away_score_list.append(away_score)
                            play_number.append(int(play_count))
                            play_count = play_count + 1
                            
                            m, s = clock.split(':')
                            game_time = 0.1
                            quarter = 4
                            ot_flag = 1
                             
                            if home_score > away_score:
                                cur_home_win_probability = 100
                                cur_away_win_probability = 100 - cur_home_win_probability
                                home_win_probability.append(cur_home_win_probability)
                                away_win_probability.append(cur_away_win_probability)
                            elif home_score < away_score:
                                cur_away_win_probability = 100
                                cur_home_win_probability = 100 - cur_away_win_probability
                                away_win_probability.append(cur_away_win_probability)
                                home_win_probability.append(cur_home_win_probability)
                            break
                            
    plot_score_plot_thread_crawler(home_team, away_team, home_score_list, away_score_list, play_number, home_color, away_color)
    plot_win_probability_thread_crawler(home_team, away_team, home_win_probability, away_win_probability, play_number, home_color, away_color)