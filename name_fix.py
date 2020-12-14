#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix the names of teams so that they align with what the Reddit game thread and Google Sheet
expect

@author: apkick
"""

"""
Change team from what Reddit expects so that it can match with Google sheets

"""
def handleNamingInconsistincies(team):
    if(team.find('amp;') >= 0):
        team = team.replace('amp;', '')
    if(team.find('–') >= 0):
        team = team.replace('–', '-')
    if(team == "UMass"):
        team = "Massachusetts"
    if(team == "Southern Mississippi"):
        team = "Southern Miss"
    if(team == "Miami (FL)"):
        team = "Miami"
    if(team == "Miami (OH)"):
        team = "Miami, OH"
    return team

"""
Change the user input team so that it can match for Reddit Game Threads

"""
def changeUserInputTeams(team):
    if((team == "Texas A&M") and (team.find('A&M') >= 0 or team.find('a&m') >= 0)):
        team = team.replace('&', '&amp;')
    if(team == 'Miami' or team == 'miami'):
        team = 'miami (fl)'
    if(team == 'Southern Miss' or team == 'southern miss'):
        team = 'southern mississippi'
    return team
