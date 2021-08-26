import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

"""
Plot graphs using MatPlotLib

@author: apkick
"""

"""
Plot the win probability for the game using Gist data

"""
def plot_win_probability_gist(home_team, away_team, home_win_probability, away_win_probability, play_number, home_color, away_color):
    play_number = np.array(play_number)
    home_win_probability = np.array(home_win_probability)
    away_win_probability = np.array(away_win_probability)

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw=dict(wspace=0.0, hspace=0, bottom=0.5 / (2 + 1), left=0.5 / (3)))
    l1 = ax1.plot(play_number, home_win_probability, home_color, linewidth=2)
    l2 = ax2.plot(play_number, away_win_probability, away_color, linewidth=2)

    ax2.invert_yaxis()
    lim = max(max(ax1.get_ylim()), max(ax2.get_ylim()))
    ax1.set_ylim(50, lim)
    ax2.set_ylim(lim, 50)
    plt.legend(l1+l2, [home_team, away_team])

    plt.style.use('fivethirtyeight')
    plt.ylabel("Win Probability (%)")
    plt.xlabel("Play")
    top_ticks = [50, 60, 70, 80, 90, 100]
    bottom_ticks = [50, 60, 70, 80, 90, 100]
    ax1.set_yticks(top_ticks)
    ax2.set_yticks(bottom_ticks)
    ax1.set_title("Win Probability", loc="center")
    ax1.axhline(y=50, ls='-', color = "black")
    ax2.axhline(y=50, ls='-', color = "black")
    ax1.legend(l1, [home_team], loc="upper left")
    ax2.legend(l2, [away_team], loc="lower left")
    plt.savefig("outputwin_probability.png")
    plt.close()
    
"""
Plot the score progression for the game using Gist data

"""
def plot_score_gist(home_team, away_team, homeScore, awayScore, play_number, home_color, away_color, OTFlag):
    play_number = np.array(play_number)
    homeScore = np.array(homeScore)
    awayScore = np.array(awayScore)

    plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylabel("Score")
    if(OTFlag == 1):
        plt.xlabel("Play Number")
        plt.title("Score Plot (OT)")
        plt.plot(play_number, homeScore, color = home_color, label = home_team, linewidth=2)
        plt.plot(play_number, awayScore, color = away_color, label = away_team, linewidth=2)
    else:
        plt.xlabel("Play")
        plt.title("Score Plot")
        plt.plot(play_number, homeScore, color=home_color, label=home_team, linewidth=2)
        plt.plot(play_number, awayScore, color=away_color, label=away_team, linewidth=2)
        
    plt.legend(loc="upper left")
    plt.savefig("output.png")
    plt.close()

"""
Plot the win probability for the game using Thread Crawler data

"""
def plot_win_probability_thread_crawler(home_team, away_team, home_win_probability, away_win_probability, play_number, home_color, away_color):
    play_number = np.array(play_number)
    home_win_probability = np.array(home_win_probability)
    away_win_probability = np.array(away_win_probability)
    
    plt.figure()
    plt.style.use('fivethirtyeight')
    plt.ylabel("Win Probability (%)")
    plt.xlabel("")
    plt.title("Win Probability")
    plt.plot(play_number, home_win_probability, color = home_color, label = home_team)
    plt.plot(play_number, away_win_probability, color = away_color, label = away_team)
    plt.ylim(-10, 110)
    plt.xticks([])
    plt.legend(loc="upper left")
    plt.savefig("outputwin_probability.png")
    plt.close()
    
"""
Plot the score progression for the game using Thread Crawler data

"""
def plot_score_thread_crawler(home_team, away_team, homeScore, awayScore, play_number, home_color, away_color):      
    play_number = np.array(play_number)
    homeScore = np.array(homeScore)
    awayScore = np.array(awayScore)

    plt.style.use('fivethirtyeight')
    plt.ylabel("Score")
    plt.xlabel("")
    plt.title("Score Plot")
    plt.plot(play_number, homeScore, color = home_color, label = home_team)
    plt.plot(play_number, awayScore, color = away_color, label = away_team)
    plt.xticks([])   
    plt.legend(loc="upper left")
    plt.savefig("output.png")
    plt.close()
    
    