from winProbability import calculateWinProbabilityThreadCrawler
from winProbability import calculateExpectedPoints
from plotGraphs import plotScorePlotThreadCrawler
from plotGraphs import plotWinProbabilityThreadCrawler

"""
Crawl through an old Game Thread (pre-Season 4) and gather game data and plot it

@author: apkick
"""


"""
Crawl through old season threads and plot the win probability and score

"""
def threadCrawler(homeTeam, awayTeam, homeVegasOdds, awayVegasOdds, homeColor, awayColor, season, submission):
    submission.comment_sort = "old"

    if(homeTeam.find('-') >= 0):
        homeTeam = homeTeam.replace('-', '–')
    if(awayTeam.find('-') >= 0):
        awayTeam = awayTeam.replace('-', '–')
    
    if(homeTeam == "Massachusetts"):
        homeTeam = "UMass"
    elif(awayTeam == "Massachusetts"):
        awayTeam = "UMass"
    
    homeUser = ""
    awayUser = ""
    homeScore = 0
    awayScore = 0
    OTFlag = 0
    quarter = 1
    clock = "7:00"
    yardLine = 25
    possession = "home"
    down = 1
    distance = 10
    playType = "EMPTY"
    data = ""
    homeScoreList = []
    awayScoreList = []
    homeWinProbability = []
    awayWinProbability = []
    playNumber = []
    playCount = 1
    submission.comments.replace_more(limit=0)
    for comment in submission.comments:
        if(OTFlag == 1):
            break
        if(comment.author == 'NFCAAOfficialRefBot' and 'you\'re home' in comment.body):
            homeUser = comment.body.split("The game has started!")[1].split(",")[0].strip()
            awayUser = comment.body.split("The game has started!")[1].split(",")[1].split("home. ")[1].strip()
        #Handle delay of game
        if(comment.author == 'NFCAAOfficialRefBot' and 'not sent their number in over 24 hours' in comment.body
           and "touchdown" in comment.body):
            if(homeUser in comment.body):
                awayScore = awayScore + 8
                playType = "PAT"
                   
                homeScoreList.append(homeScore)
                awayScoreList.append(awayScore)
                playNumber.append(int(playCount))
                playCount = playCount + 1
                                
                m, s = clock.split(':')
                time = int(m) * 60 + int(s)
                                
                expectedPoints = calculateExpectedPoints(int(down), int(distance), int(yardLine), playType)  
                if(possession == "home"):
                    curHomeWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, homeScore, awayScore, int(down), int(distance), int(yardLine), playType, homeVegasOdds) * 100
                    curAwayWinProbability = 100 - curHomeWinProbability
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(curAwayWinProbability)
                elif(possession == "away"):
                    curAwayWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, awayScore, homeScore, int(down), int(distance), int(yardLine), playType, awayVegasOdds) * 100
                    curHomeWinProbability = 100 - curAwayWinProbability
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(curHomeWinProbability) 
                data = (str(homeScore) + " | " + str(awayScore) + " | " + str(quarter) + " | " + clock + " | " 
                                  + str(yardLine) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + playType)
                
            if(awayUser in comment.body):
                homeScore = homeScore + 8
                playType = "PAT"
               
                homeScoreList.append(homeScore)
                awayScoreList.append(awayScore)
                playNumber.append(int(playCount))
                playCount = playCount + 1
                            
                m, s = clock.split(':')
                time = int(m) * 60 + int(s)
                            
                expectedPoints = calculateExpectedPoints(int(down), int(distance), int(yardLine), playType)  
                if(possession == "home"):
                    curHomeWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, homeScore, awayScore, int(down), int(distance), int(yardLine), playType, homeVegasOdds) * 100
                    curAwayWinProbability = 100 - curHomeWinProbability
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(curAwayWinProbability)
                elif(possession == "away"):
                    curAwayWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, awayScore, homeScore, int(down), int(distance), int(yardLine), playType, awayVegasOdds) * 100
                    curHomeWinProbability = 100 - curAwayWinProbability
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(curHomeWinProbability)
                data = (str(homeScore) + " | " + str(awayScore) + " | " + str(quarter) + " | " + clock + " | " 
                                  + str(yardLine) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + playType)
                
        if(comment.author == 'NFCAAOfficialRefBot' and 'not sent their number in over 24 hours' in comment.body
           and "touchdown" in comment.body):
            if(homeUser in comment.body):
                awayScore = awayScore
                   
                homeScoreList.append(homeScore)
                awayScoreList.append(awayScore)
                playNumber.append(int(playCount))
                playCount = playCount + 1
                                
                m, s = clock.split(':')
                time = int(m) * 60 + int(s)
                                
                expectedPoints = calculateExpectedPoints(int(down), int(distance), int(yardLine), playType)  
                if(possession == "home"):
                    curHomeWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, awayScore, homeScore, int(down), int(distance), int(yardLine), playType, homeVegasOdds) * 100
                    curAwayWinProbability = 100 - curHomeWinProbability
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(curAwayWinProbability)
                elif(possession == "away"):
                    curAwayWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, homeScore, awayScore, int(down), int(distance), int(yardLine), playType, awayVegasOdds) * 100
                    curHomeWinProbability = 100 - curAwayWinProbability
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(curHomeWinProbability) 
                data = (str(homeScore) + " | " + str(awayScore) + " | " + str(quarter) + " | " + clock + " | " 
                                  + str(yardLine) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + playType)
                
            if(awayUser in comment.body):
                homeScore = homeScore
               
                homeScoreList.append(homeScore)
                awayScoreList.append(awayScore)
                playNumber.append(int(playCount))
                playCount = playCount + 1
                            
                m, s = clock.split(':')
                time = int(m) * 60 + int(s)
                            
                expectedPoints = calculateExpectedPoints(int(down), int(distance), int(yardLine), playType)  
                if(possession == "home"):
                    curHomeWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, homeScore, awayScore, int(down), int(distance), int(yardLine), playType, homeVegasOdds) * 100
                    curAwayWinProbability = 100 - curHomeWinProbability
                    homeWinProbability.append(curHomeWinProbability)
                    awayWinProbability.append(curAwayWinProbability)
                elif(possession == "away"):
                    curAwayWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, awayScore, homeScore, int(down), int(distance), int(yardLine), playType, awayVegasOdds) * 100
                    curHomeWinProbability = 100 - curAwayWinProbability
                    awayWinProbability.append(curAwayWinProbability)
                    homeWinProbability.append(curHomeWinProbability)
                data = (str(homeScore) + " | " + str(awayScore) + " | " + str(quarter) + " | " + clock + " | " 
                                  + str(yardLine) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + playType)
                   
        # Look through top level comment
        if(comment.author == 'NFCAAOfficialRefBot' and 'has submitted their' in comment.body and OTFlag != 1):
            if(OTFlag == 1):
                break
            # Get the clock and quarter
            clock = comment.body.split("left in the")[0].split("on the")[-1].split(". ")[-1]
            quarter = comment.body.split("left in the ")[1].split(".")[0]
            if(quarter == "1st"):
                quarter = 1
            elif(quarter == "2nd"):
                quarter = 2
            elif(quarter == "3rd"):
                quarter = 3
            elif(quarter == "4th"):
                quarter = 4
            
            # Handle non kickoff and PATs
            if("kicking off" not in comment.body and "PAT" not in comment.body):
                # Get the down and distance
                down = comment.body.split("It\'s ")[-1].split(" and")[0]
                distance = comment.body.split("It\'s ")[-1].split(" and ")[1].split("on the")[0].strip()
                if(down == "1st"):
                    down = 1
                elif(down == "2nd"):
                    down = 2
                elif(down == "3rd"):
                    down = 3
                elif(down == "4th"):
                    down = 4
                    
                # Get the current possession
                possessionUser = comment.body.split(" reply ")[0].split("\n")[-1]
                if(possessionUser == homeUser):
                    possession = "home"
                elif(possessionUser == awayUser):
                    possession = "away"
                
                # Get the current yard line
                if("50" not in comment.body.split(" on the ")[1].split(".")[0].split(" ")):
                    yardLine = comment.body.split(" on the ")[1].split(".")[0].split(" ")[-1]
                    sideOfField = ""
                    for item in comment.body.split(" on the ")[1].split(".")[0].split(" ")[:-1]:
                        sideOfField = sideOfField + " " + item
                    sideOfField = sideOfField.strip()
                    if(possession == "home" and sideOfField == awayTeam):
                        yardLine = 100-int(yardLine)
                    elif(possession == "away" and sideOfField == homeTeam):
                        yardLine = 100-int(yardLine)
                else:
                    yardLine = 50
                
                # Handle "and goal" situations
                if(distance == "goal"):
                    distance = 100-int(yardLine)             
            else:
                down = 1
                distance = 10
            if("kicking off" in comment.body):
                yardLine = 35
                possessionUser = comment.body.split(" reply ")[0].split("\n")[-1]
                if(possessionUser == homeUser):
                    possession = "home"
                elif(possessionUser == awayUser):
                    possession = "away"
                
            if("PAT" in comment.body):
                yardLine = 97
                possessionUser = comment.body.split(" reply ")[0].split("\n")[-1]
                if(possessionUser == homeUser):
                    possession = "home"
                elif(possessionUser == awayUser):
                    possession = "away"
            for secondLevelComment in comment.replies:
                if(OTFlag == 1):
                    break
                # Look through second level comment  
                if(" and " in homeUser):
                    homeUser1 = homeUser.split(" and ")[0]
                    homeUser2 = homeUser.split(" and ")[1]
                else:
                    homeUser1 = homeUser
                    homeUser2 = "BLANK USER"
                if(" and " in awayUser):
                    awayUser1 = awayUser.split(" and ")[0]
                    awayUser2 = awayUser.split(" and ")[1]
                else:
                    awayUser1 = awayUser
                    awayUser2 = "BLANK USER"
                if(secondLevelComment.author == homeUser1.split("/u/")[-1] or secondLevelComment.author == awayUser1.split("/u/")[-1]
                   or secondLevelComment.author == homeUser2.split("/u/")[-1] or secondLevelComment.author == awayUser2.split("/u/")[-1]):
                    commentList = secondLevelComment.body.split(" ")
                    if(OTFlag == 1):
                        break
                    commentList = [x.lower() for x in commentList]
                    if("normal" in commentList):
                        playType = "KICKOFF_NORMAL"
                    elif("squib" in commentList):
                        playType = "KICKOFF_SQUIB"
                    elif("onside" in commentList):
                        playType = "KICKOFF_ONSIDE"  
                    elif("pat" in commentList):
                        playType = "PAT"
                    elif("two" in commentList and "point" in commentList):
                        playType = "TWO_POINT"
                    else:
                        playType = "EMPTY"
                    for thirdLevelComment in secondLevelComment.replies:
                        if(season != "S1"):
                            #Look through third level comments
                            if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The two point was successful' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The two point was successful' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body 
                               and 'PAT or two point' not in thirdLevelComment.body and awayUser in thirdLevelComment.body):
                                homeScore = homeScore + 6
                                playType = "PAT"
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body
                               and 'PAT or two point' not in thirdLevelComment.body and homeUser in thirdLevelComment.body):
                                awayScore = awayScore + 6
                                playType = "PAT"
                        elif(season == "S1"):
                            #Look through third level comments
                            if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and homeTeam + " is kicking off"  in thirdLevelComment.body):
                                homeScore = homeScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'The PAT was successful' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 1
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and ('The two point was successful' in thirdLevelComment.body
                                 or 'The two point conversion is successful' in thirdLevelComment.body)
                                 and homeTeam + " is kicking off" in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and ('The two point was successful' in thirdLevelComment.body
                                 or 'The two point conversion is successful' in thirdLevelComment.body)
                                 and homeTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'safety' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                homeScore = homeScore + 2
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and homeTeam + " is kicking off" in thirdLevelComment.body):
                                homeScore = homeScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'field goal is good' in thirdLevelComment.body
                               and awayTeam + " is kicking off" in thirdLevelComment.body):
                                awayScore = awayScore + 3
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body 
                               and homeTeam + " just scored." in thirdLevelComment.body):
                                homeScore = homeScore + 6
                                playType = "PAT"
                            elif(thirdLevelComment.author == 'NFCAAOfficialRefBot' and 'just scored' in thirdLevelComment.body
                               and awayTeam + " just scored." in thirdLevelComment.body):
                                awayScore = awayScore + 6
                                playType = "PAT"
                        if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and  "we're going to overtime!" in thirdLevelComment.body):
                            OTFlag = 0
                            break
                        # Add data
                        if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and "I'm not waiting on a message from you" not in thirdLevelComment.body):
                            #Fill plot data
                            data = (str(homeScore) + " | " + str(awayScore) + " | " + str(quarter) + " | " + clock + " | " 
                                  + str(yardLine) + " | " + possession + " | " + str(down) + " | " + str(distance) + " | "
                                  + playType)
                            print(data)
                            homeScoreList.append(homeScore)
                            awayScoreList.append(awayScore)
                            playNumber.append(int(playCount))
                            playCount = playCount + 1
                            
                            m, s = clock.split(':')
                            time = int(m) * 60 + int(s)
                            if(time == 0 and int(quarter) == 4):
                                if(homeScore > awayScore):
                                    curHomeWinProbability = 100
                                    urAwayWinProbability = 100 - curHomeWinProbability
                                    homeWinProbability.append(curHomeWinProbability)
                                    awayWinProbability.append(curAwayWinProbability)
                                elif(homeScore < awayScore):
                                    curAwayWinProbability = 100
                                    curHomeWinProbability = 100 - curAwayWinProbability
                                    awayWinProbability.append(curAwayWinProbability)
                                    homeWinProbability.append(curHomeWinProbability)
                                break
                            expectedPoints = calculateExpectedPoints(int(down), int(distance), int(yardLine), playType)  
                            if(possession == "home"):
                                curHomeWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, homeScore, awayScore, int(down), int(distance), int(yardLine), playType, homeVegasOdds) * 100
                                curAwayWinProbability = 100 - curHomeWinProbability
                                homeWinProbability.append(curHomeWinProbability)
                                awayWinProbability.append(curAwayWinProbability)
                            elif(possession == "away"):
                                curAwayWinProbability = calculateWinProbabilityThreadCrawler(expectedPoints, int(quarter), time, awayScore, homeScore, int(down), int(distance), int(yardLine), playType, awayVegasOdds) * 100
                                curHomeWinProbability = 100 - curAwayWinProbability
                                awayWinProbability.append(curAwayWinProbability)
                                homeWinProbability.append(curHomeWinProbability) 
                            
                        # If end of game, make sure WP is 100% and 0%
                        if(thirdLevelComment.author == 'NFCAAOfficialRefBot' and "that's the end of the game" in thirdLevelComment.body):
                            homeScoreList.append(homeScore)
                            awayScoreList.append(awayScore)
                            playNumber.append(int(playCount))
                            playCount = playCount + 1
                            
                            m, s = clock.split(':')
                            time = 0.1
                            quarter = 4
                            OTFlag = 1
                             
                            if(homeScore > awayScore):
                                curHomeWinProbability = 100
                                curAwayWinProbability = 100 - curHomeWinProbability
                                homeWinProbability.append(curHomeWinProbability)
                                awayWinProbability.append(curAwayWinProbability)
                            elif(homeScore < awayScore):
                                curAwayWinProbability = 100
                                curHomeWinProbability = 100 - curAwayWinProbability
                                awayWinProbability.append(curAwayWinProbability)
                                homeWinProbability.append(curHomeWinProbability)
                            break
                            
    plotScorePlotThreadCrawler(homeTeam, awayTeam, homeScoreList, awayScoreList, playNumber, homeColor, awayColor)
    plotWinProbabilityThreadCrawler(homeTeam, awayTeam, homeWinProbability, awayWinProbability, playNumber, homeColor, awayColor)