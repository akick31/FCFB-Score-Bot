#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:38:06 2020

@author: apkick
"""

from reddit_login import login_reddit
from discord_function import login_discord


# Main method
if __name__ == '__main__':
    r = login_reddit()
    login_discord(r)