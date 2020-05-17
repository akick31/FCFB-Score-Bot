#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:38:06 2020

@author: apkick
"""

from redditLogin import loginReddit
from discordFunction import loginDiscord


# Main method
if __name__ == '__main__':
    r = loginReddit()
    loginDiscord(r)