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
Get all team information and post it as an embed

"""



def get_team_information(database, team):
    division = get_team_division(database, team)
    if division == "FCS":
        return "Our apologies, FCS teams are not currently supported. Please try again later"
    elif division != "FBS":
        return "Error: Could not find team in FBS or FCS subdivisions, are you sure you typed the name correctly?"
    
    current_coach = get_team_current_coach(database, team, division)
    number_of_coaches = get_team_number_of_coaches(database, team, division)
    winningest_coach = get_team_winningest_coach(database, team, division)
    longest_serving_coach = get_team_longest_serving_coach(database, team, division)
    wins = get_team_wins(database, team, division)
    losses = get_team_losses(database, team, division)

    print("SUCCESS! Fetched all team information from database!")
    return wins
