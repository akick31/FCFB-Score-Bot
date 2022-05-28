# importing required libraries
import mysql.connector
import json
import tabulate
import discord
from tabulate import tabulate
tabulate.PRESERVE_WHITESPACE = True


"""
Connect to the MySQL FCFB database

"""


def connect_to_database():
    with open('/home/ubuntu/FCFB/FCFB-Score-Bot/config.json', 'r') as config_file:
        config_data = json.load(config_file)
    password = config_data['database_password']

    database = mysql.connector.connect(
    host ="localhost",
    user ="apkick",
    passwd =password,
    database = "fcfb"
    )

    if database.is_connected():
        print('\nConnected to the FCFB database')
        return database
    else:
        print('\nNot connected to FCFB database!')
        return None


"""
Close the database

"""


def close_database(database):
    database.commit()
    database.close()


"""
Put together a team's record in a string for viewing

"""


def get_record(wins, losses):
    return (str(wins) + "-" + str(losses))



"""
Return the team elo

"""



def get_elo(database, team):
    cursor = database.cursor(buffered=True)

    cursor.execute(""" SELECT * FROM FBS_ELO """)
    fbs_elo = cursor.fetchall()

    for row in fbs_elo:
        if row[0] == team:
            cursor.close()
            print("SUCCESS! Fetched ELO from database")
            return row[1]
    cursor.close()

    cursor = database.cursor()
    cursor.execute(""" SELECT * FROM FCS_ELO """)
    fcs_elo = cursor.fetchall()

    for row in fcs_elo:
        if row[0] == team:
            cursor.close()
            print("SUCCESS! Fetched ELO from database")
            return row[1]

    print("Error: Could not find ELO for " + team)
    cursor.close()
    return None


"""
Return the elo rankings

"""



def get_elo_rankings(database, post, table_name):
    cursor = database.cursor(buffered=True)
    
    cursor.execute(""" SELECT * FROM """ + table_name + """ ORDER BY ELO DESC""")
    elo = cursor.fetchall()

    rank = 1
    post_data = []
    for row in elo:
        if row[2] is not None:
            row_data = [rank, row[0], row[1], row[2]]
            post_data.append(row_data)
        else:
            row_data = [rank, row[0], row[1], "0"]
            post_data.append(row_data)
        rank = rank + 1
        if rank == 26:
            cursor.close()
            post = post + tabulate(post_data, headers=["Rank", "Team", "ELO", " ± "], tablefmt="pretty", colalign=("center", "left", "center", "center")) + "\n```"
            return post
    
    print("SUCCESS! Fetched ELO rankings from database")
    cursor.close()
    return None



"""
Get specific team information

"""



def get_team_division(database, team):
    cursor = database.cursor(buffered=True)
    team = team.strip()

    cursor.execute("""SELECT name FROM FBS_teams""")
    fbs_teams = cursor.fetchall()
    for fbs_team in fbs_teams:
        if team == fbs_team[0].lower():
            cursor.close()
            return "FBS"
    
    cursor.execute("""SELECT name FROM FCS_teams""")
    fcs_teams = cursor.fetchall()
    for fcs_team in fcs_teams:
        if team == fcs_team[0].lower():
            cursor.close()
            return "FCS"
    else:
        cursor.close()
        return None


"""
Get team win information

"""



def get_team_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched wins from database!")
    return information_requested[0]


"""
Get team loss information

"""



def get_team_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched losses from database!")
    return information_requested[0]


"""
Get team coach information

"""



def get_team_current_coach(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT current_coach FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT current_coach FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched current_coach from database!")
    return information_requested[0]


"""
Get number of coaches a team has had

"""



def get_team_number_of_coaches(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT number_of_coaches FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT number_of_coaches FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched number_of_coaches from database!")
    return information_requested[0]


"""
Get winningest coach at a team

"""



def get_team_winningest_coach(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT winningest_coach FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT winningest_coach FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched winningest_coach from database!")
    return information_requested[0]


"""
Get longest tenured coach at a team

"""



def get_team_longest_serving_coach(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT longest_serving_coach FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT longest_serving_coach FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched longest_serving_coach from database!")
    return information_requested[0]


"""
Get team winning percentage

"""



def get_team_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched win_percentage from database!")
    return information_requested[0]


"""
Get team conference win information

"""



def get_team_conference_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT conference_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT conference_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched conference_wins from database!")
    return information_requested[0]


"""
Get team conference loss information

"""



def get_team_conference_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT conference_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT conference_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched conference_losses from database!")
    return information_requested[0]


"""
Get team conference winning percentage

"""



def get_team_conference_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT conference_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT conference_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched conference_win_percentage from database!")
    return information_requested[0]


"""
Get team division win information

"""



def get_team_division_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT division_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT division_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched division_wins from database!")
    return information_requested[0]


"""
Get team division loss information

"""



def get_team_division_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT division_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT division_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched division_losses from database!")
    return information_requested[0]


"""
Get team division winning percentage

"""



def get_team_division_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT division_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT division_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched division_win_percentage from database!")
    return information_requested[0]


"""
Get team ooc win information

"""



def get_team_ooc_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT ooc_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT ooc_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched ooc_wins from database!")
    return information_requested[0]


"""
Get team ooc loss information

"""



def get_team_ooc_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT ooc_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT ooc_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched ooc_losses from database!")
    return information_requested[0]


"""
Get team ooc winning percentage

"""



def get_team_ooc_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT ooc_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT ooc_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched ooc_win_percentage from database!")
    return information_requested[0]


"""
Get team ranked win information

"""



def get_team_ranked_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT ranked_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT ranked_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched ranked_wins from database!")
    return information_requested[0]


"""
Get team ranked loss information

"""



def get_team_ranked_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT ranked_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT ranked_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched ranked_losses from database!")
    return information_requested[0]


"""
Get team ranked winning percentage

"""



def get_team_ranked_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT ranked_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT ranked_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched ranked_win_percentage from database!")
    return information_requested[0]


"""
Get team wins as ranked information

"""



def get_team_wins_as_ranked(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT wins_as_ranked FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT wins_as_ranked FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched wins_as_ranked from database!")
    return information_requested[0]


"""
Get team losses as information

"""



def get_team_losses_as_ranked(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT losses_as_ranked FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT losses_as_ranked FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched losses_as_ranked from database!")
    return information_requested[0]


"""
Get team winning percentage as ranked

"""



def get_team_win_percentage_as_ranked(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT win_percentage_as_ranked FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT win_percentage_as_ranked FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched win_percentage_as_ranked from database!")
    return information_requested[0]


"""
Get highest rank a team has had

"""



def get_team_highest_rank(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT highest_rank FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT highest_rank FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched highest_rank from database!")
    return information_requested[0]


"""
Get number of weeks a team has been ranked

"""



def get_team_weeks_ranked(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT weeks_ranked FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT weeks_ranked FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched weeks_ranked from database!")
    return information_requested[0]


"""
Get team bowl win information

"""



def get_team_bowl_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT bowl_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT bowl_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched bowl_wins from database!")
    return information_requested[0]


"""
Get team bowl loss information

"""



def get_team_bowl_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT bowl_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT bowl_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched bowl_losses from database!")
    return information_requested[0]


"""
Get team bowl winning percentage

"""



def get_team_bowl_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT bowl_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT bowl_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched bowl_win_percentage from database!")
    return information_requested[0]


"""
Get team bowl win information

"""



def get_team_conference_championship_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT conference_championship_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT conference_championship_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched conference_championship_wins from database!")
    return information_requested[0]


"""
Get team bowl loss information

"""



def get_team_conference_championship_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT conference_championship_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT conference_championship_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched conference_championship_losses from database!")
    return information_requested[0]


"""
Get team bowl winning percentage

"""



def get_team_conference_championship_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT conference_championship_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT conference_championship_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched conference_championship_win_percentage from database!")
    return information_requested[0]


"""
Get number of playoff appearances for a team

"""



def get_team_playoff_appearances(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT playoff_appearances FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT playoff_appearances FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched playoff_appearances from database!")
    return information_requested[0]


"""
Get team bowl win information

"""



def get_team_playoff_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT playoff_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT playoff_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched playoff_wins from database!")
    return information_requested[0]


"""
Get team playoff loss information

"""



def get_team_playoff_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT playoff_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT playoff_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched playoff_losses from database!")
    return information_requested[0]


"""
Get team playoff winning percentage

"""



def get_team_playoff_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT playoff_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT playoff_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched playoff_win_percentage from database!")
    return information_requested[0]


"""
Get team national_championship win information

"""



def get_team_national_championship_wins(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT national_championship_wins FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT national_championship_wins FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched national_championship_wins from database!")
    return information_requested[0]


"""
Get team national_championship loss information

"""



def get_team_national_championship_losses(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT national_championship_losses FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT national_championship_losses FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched national_championship_losses from database!")
    return information_requested[0]


"""
Get team playoff winning percentage

"""



def get_team_national_championship_win_percentage(database, team, division):
    cursor = database.cursor(buffered=True)

    if division == "FBS":
        cursor.execute(""" SELECT national_championship_win_percentage FROM FBS_teams WHERE name = '""" + team + "'")
    elif division == "FCS":
        cursor.execute(""" SELECT national_championship_win_percentage FROM FCS_teams WHERE name = '""" + team + "'")
    information_requested = cursor.fetchall()

    cursor.close()
    print("Success! Fetched national_championship_win_percentage from database!")
    return information_requested[0]


"""
Get all team information and post it as an embed

"""



def get_team_information(database, team):
    division = get_team_division(database, team)
    if division == "FCS":
        return "Our apologies, FCS teams are not currently supported. Please try again later"
    elif division != "FBS":
        return "Error: Could not find team in FBS or FCS subdivisions, are you sure you typed the name correctly?"
    
    # Gather all the information from the DB
    current_coach = get_team_current_coach(database, team, division)[0]
    number_of_coaches = get_team_number_of_coaches(database, team, division)[0]
    winningest_coach = get_team_winningest_coach(database, team, division)[0]
    longest_serving_coach = get_team_longest_serving_coach(database, team, division)[0]
    wins = get_team_wins(database, team, division)[0]
    losses = get_team_losses(database, team, division)[0]
    all_time_record = get_record(wins, losses)
    win_percentage = get_team_win_percentage(database, team, division)[0]
    conference_wins = get_team_conference_wins(database, team, division)[0]
    conference_losses = get_team_conference_losses(database, team, division)[0]
    conference_record = get_record(conference_wins, conference_losses)
    conference_win_percentage = get_team_conference_win_percentage(database, team, division)[0]
    division_wins = get_team_division_wins(database, team, division)[0]
    division_losses = get_team_division_losses(database, team, division)[0]
    division_record = get_record(division_wins, division_losses)
    division_win_percentage = get_team_division_win_percentage(database, team, division)[0]
    ooc_wins = get_team_ooc_wins(database, team, division)[0]
    ooc_losses = get_team_ooc_losses(database, team, division)[0]
    ooc_record = get_record(ooc_wins, ooc_losses)
    ooc_win_percentage = get_team_ooc_win_percentage(database, team, division)[0]
    ranked_wins = get_team_ranked_wins(database, team, division)[0]
    ranked_losses = get_team_ranked_losses(database, team, division)[0]
    ranked_record = get_record(ranked_wins, ranked_losses)
    ranked_win_percentage = get_team_ranked_win_percentage(database, team, division)[0]
    wins_as_ranked = get_team_wins_as_ranked(database, team, division)[0]
    losses_as_ranked = get_team_losses_as_ranked(database, team, division)[0]
    record_as_ranked = get_record(wins_as_ranked, losses_as_ranked)
    win_percentage_as_ranked = get_team_win_percentage_as_ranked(database, team, division)[0]
    highest_rank = get_team_highest_rank(database, team, division)[0]
    weeks_ranked = get_team_weeks_ranked(database, team, division)[0]
    bowl_wins = get_team_bowl_wins(database, team, division)[0]
    bowl_losses = get_team_bowl_losses(database, team, division)[0]
    bowl_record = get_record(bowl_wins, bowl_losses)
    bowl_win_percentage = get_team_bowl_win_percentage(database, team, division)[0]
    conference_championship_wins = get_team_conference_championship_wins(database, team, division)[0]
    conference_championship_losses = get_team_conference_championship_losses(database, team, division)[0]
    conference_championship_record = get_record(conference_championship_wins, conference_championship_losses)
    conference_championship_win_percentage = get_team_conference_championship_win_percentage(database, team, division)[0]
    playoff_appearances = get_team_playoff_appearances(database, team, division)[0]
    playoff_wins = get_team_playoff_wins(database, team, division)[0]
    playoff_losses = get_team_playoff_losses(database, team, division)[0]
    playoff_record = get_record(playoff_wins, playoff_losses)
    playoff_win_percentage = get_team_playoff_win_percentage(database, team, division)[0]
    national_championship_wins = get_team_national_championship_wins(database, team, division)[0]

    information_list = [current_coach, number_of_coaches, winningest_coach, 
    longest_serving_coach, all_time_record, win_percentage, conference_record, 
    conference_win_percentage, division_record, division_win_percentage, 
    ooc_record, ooc_win_percentage, ranked_record, ranked_win_percentage,
    record_as_ranked, win_percentage_as_ranked, highest_rank, weeks_ranked,
    bowl_record, bowl_win_percentage, conference_championship_record, 
    conference_championship_win_percentage, playoff_appearances, playoff_record,
    playoff_win_percentage, national_championship_wins]

    print("Success! Fetched all team information from database!")
    return information_list
