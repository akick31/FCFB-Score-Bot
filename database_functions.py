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

    cursor.execute("""SELECT name FROM FBS_teams""")
    fbs_teams = cursor.fetchall()
    if team in fbs_teams:
        cursor.close()
        return "FBS"
    
    cursor.execute("""SELECT name FROM FCS_teams""")
    fbs_teams = cursor.fetchall()
    if team in fbs_teams:
        cursor.close()
        return "FCS"
    else
        cursor.close()
        return None


"""
Get specific team information

"""



def get_fbs_team_specific_information(database, team, information):
    cursor = database.cursor(buffered=True)

    sql = """SELECT %s FROM FBS_teams WHERE name = %s"""
    val = (information, team)
    cursor.execute(sql, val)
    information = cursor.fetchall()
    
    cursor.close()
    print("SUCCESS! Fetched " + information + "from database")
    return information


"""
Get all team information and post it as an embed

"""



def get_fbs_team_all_information(database, team, information):
    cursor = database.cursor(buffered=True)

    sql = """SELECT %s FROM FBS_teams WHERE name = %s"""
    val = (information, team)
    cursor.execute(sql, val)
    information = cursor.fetchall()
    
    cursor.close()
    print("SUCCESS! Fetched " + information + "from database")
    return information
