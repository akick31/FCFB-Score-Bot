import numpy as np
import matplotlib.pyplot as plt

"""
Plot graphs using MatPlotLib

@author: apkick
"""

"""
Plot the win probability for the game using Gist data

"""
def plotWinProbabilityGist(homeTeam, awayTeam, homeWinProbability, awayWinProbability, playNumber, homeColor, awayColor):
    playNumber = np.array(playNumber)
    homeWinProbability = np.array(homeWinProbability)
    awayWinProbability = np.array(awayWinProbability)
    
    plt.figure()
    plt.ylabel("Win Probability (%)")
    plt.xlabel("")
    plt.title("Win Probability")
    plt.plot(playNumber, homeWinProbability, color = homeColor, label = homeTeam)
    plt.plot(playNumber, awayWinProbability, color = awayColor, label = awayTeam)
    plt.ylim(-10, 110)
    plt.xticks([])
    plt.legend(loc="upper left")
    plt.savefig("outputwin_probability.png")
    plt.close()
    
"""
Plot the score progression for the game using Gist data

"""
def plotScorePlotGist(x, homeTeam, awayTeam, homeScore, awayScore, playNumber, homeColor, awayColor, OTFlag):      
    playNumber = np.array(playNumber)
    homeScore = np.array(homeScore)
    awayScore = np.array(awayScore)

    plt.figure()
    plt.ylabel("Score")
    if(OTFlag == 1):
        plt.xlabel("Play Number")
        plt.title("Score Plot (OT)")
        plt.plot(playNumber, homeScore, color = homeColor, label = homeTeam)
        plt.plot(playNumber, awayScore, color = awayColor, label = awayTeam)
    else:
        plt.xlabel("Time")
        plt.title("Score Plot")
        plt.plot(x, homeScore, color = homeColor, label = homeTeam)
        plt.plot(x, awayScore, color = awayColor, label = awayTeam)
        plt.xticks(np.arange(0, 1681, 420), ['Q1', 'Q2', 'Q3', 'Q4', 'FINAL'])
        
    plt.legend(loc="upper left")
    plt.savefig("output.png")
    plt.close()

"""
Plot the win probability for the game using Thread Crawler data

"""
def plotWinProbabilityThreadCrawler(homeTeam, awayTeam, homeWinProbability, awayWinProbability, playNumber, homeColor, awayColor):
    playNumber = np.array(playNumber)
    homeWinProbability = np.array(homeWinProbability)
    awayWinProbability = np.array(awayWinProbability)
    
    plt.figure()
    plt.ylabel("Win Probability (%)")
    plt.xlabel("")
    plt.title("Win Probability")
    plt.plot(playNumber, homeWinProbability, color = homeColor, label = homeTeam)
    plt.plot(playNumber, awayWinProbability, color = awayColor, label = awayTeam)
    plt.ylim(-10, 110)
    plt.xticks([])
    plt.legend(loc="upper left")
    plt.savefig("outputwin_probability.png")
    plt.close()
    
"""
Plot the score progression for the game using Thread Crawler data

"""
def plotScorePlotThreadCrawler(homeTeam, awayTeam, homeScore, awayScore, playNumber, homeColor, awayColor):      
    playNumber = np.array(playNumber)
    homeScore = np.array(homeScore)
    awayScore = np.array(awayScore)

    plt.ylabel("Score")
    plt.xlabel("")
    plt.title("Score Plot")
    plt.plot(playNumber, homeScore, color = homeColor, label = homeTeam)
    plt.plot(playNumber, awayScore, color = awayColor, label = awayTeam)
    plt.xticks([])   
    plt.legend(loc="upper left")
    plt.savefig("output.png")
    plt.close()
    
    