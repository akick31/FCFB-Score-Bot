import praw

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:43:26 2020

@author: apkick
"""


# Login to Reddit
def loginReddit():
    r = praw.Reddit(user_agent='ScoreboardBot by /u/akick31',
                    client_id='mbxqsh9-BGzlow',
                    client_secret='DUh4hWoT3QvsJnk3ctepVjxbDWo',
                    username='FCFBScoreBot',
                    password='goodbyerhule',
                    subreddit='FakeCollegeFootball')
    return r   