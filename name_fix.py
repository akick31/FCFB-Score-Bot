import json

with open('name_fix.json', 'r') as config_file:
    name_fix_data = json.load(config_file)


"""
Fix the names of teams so that they align with what the Reddit game thread and Google Sheet
expect

@author: apkick
"""

"""
Change team from what Reddit expects so that it can match with Google sheets

"""


def handle_naming_inconsistencies(team):
    if "amp;" in team:
        team = team.replace('amp;', '')
    if "–" in team:
        team = team.replace('–', '-')
    if team in name_fix_data["reddit_names"]:
        team = name_fix_data["reddit_names"][team]

    return team


"""
Change the user input team so that it can match for Reddit Game Threads

"""


def fix_user_input_teams(team):
    team = team.lower()
    if "a&m" in team:
        team = team.replace('&', 'amp;')
    if team in name_fix_data["user_input_fixes"]:
        team = name_fix_data["user_input_fixes"][team]

    return team
