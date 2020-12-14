#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:38:06 2020

@author: apkick
"""

from reddit_login import loginReddit
from discord_function import loginDiscord


# Main method
if __name__ == '__main__':
    r = loginReddit()
    loginDiscord(r)