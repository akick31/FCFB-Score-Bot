echo STOPPING SCORE BOT..
docker stop FCFB-Score-Bot
echo SCORE BOT STOPPED!
echo
echo REMOVING OLD SCORE BOT...
docker remove FCFB-Score-Bot
echo OLD SCORE BOT REMOVED!
echo
echo BUILDING NEW SCORE BOT...
docker build -t "fcfb-score-bot:Dockerfile" .
echo NEW SCORE BOT BUILT!
echo
echo STARTING NEW SCORE BOT...
docker run -d --restart=always --name FCFB-Score-Bot fcfb-score-bot:Dockerfile
echo NEW SCORE BOT STARTED!
echo DONE!