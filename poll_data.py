"""
Get the poll data from Reddit

@author: apkick
"""

"""
Find the post for the coaches poll

"""


def find_coaches_poll_post(r):
    search_item = "\"Coaches Poll\""
    for submission in r.subreddit("FakeCollegeFootball").search(searchItem, sort='new'):
        if "OFFICIAL COACHES' POLL" in submission.title and submission.link_flair_text == "Official":
            return submission
    return "NONE"

"""
Get the data from the coaches poll post

"""


def parse_poll(submission_body, poll_num):
    if poll_num == 0:
        poll = "**FBS Coaches Poll**"
    elif poll_num == 1:
        poll = "**FCS Coaches Poll**"
    rankings_list = submission_body.split("**FCS Poll:**")[poll_num].split("Trend")[1].split("Others receiving votes")[0]
    rankings_list = rankings_list.split(":----:|:----:|:----:|:----:|:----:|\t\t\t\t\n")[1].split("\t\t\t\t\n")
    post = ("----------------------\n" + poll + "\n----------------------\n")
    for rank in rankings_list:
        if(rank == "\n"):
            break
        line_split = rank.split(" | ")
        ranking = line_split[0].strip()
        team = line_split[1].split("[]")[0].strip()
        record = line_split[3].strip()
        post = post + ranking + " " + team + " (" + record + ")\n"
    return post


"""
Get the data and return it to the bot

"""  


def get_coaches_poll_data(r, request):
    submission = find_coaches_poll_post(r)
    if submission == "NONE":
        return "Could not find the rankings"
    elif request == "FBS":
        return parse_poll(submission.selftext, 0)
    elif request == "FCS":
        return parse_poll(submission.selftext, 1)
    


