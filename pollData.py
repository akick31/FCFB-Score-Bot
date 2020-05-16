#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get the poll data from Reddit

@author: apkick
"""

"""
Find the post for the coaches poll

"""
def findCoachesPollPost(r):
    searchItem = "\"Coaches Poll\""
    for submission in r.subreddit("FakeCollegeFootball").search(searchItem, sort='new'):
        if "OFFICIAL COACHES' POLL" in submission.title and submission.link_flair_text == "Official":
            return submission
    return "NONE"

"""
Get the data from the coaches poll post

"""
def parsePoll(submissionBody, pollNum):
    if(pollNum == 0):
        poll = "**FBS Coaches Poll**"
    elif(pollNum == 1):
        poll = "**FCS Coaches Poll**"
    rankingsList = submissionBody.split("**FCS Poll:**")[pollNum].split("Trend")[1].split("Others receiving votes")[0]
    rankingsList = rankingsList.split(":----:|:----:|:----:|:----:|:----:|\t\t\t\t\n")[1].split("\t\t\t\t\n")
    post = ("----------------------\n" + poll + "\n----------------------\n")
    for rank in rankingsList:
        if(rank == "\n"):
            break
        lineSplit = rank.split(" | ")
        ranking = lineSplit[0].strip()
        team = lineSplit[1].split("[]")[0].strip()
        record = lineSplit[3].strip()
        post = post + ranking + " " + team + " (" + record + ")\n"
    return post

"""
Get the data and return it to the bot

"""        
def getCoachesPollData(r, request):
    submission = findCoachesPollPost(r)
    if(submission == "NONE"):
        return "Could not find the rankings"
    elif(request == "FBS"):
        return parsePoll(submission.selftext, 0)
    elif(request == "FCS"):
        return parsePoll(submission.selftext, 1)
    


