"""
Picture Drawer for Fox Socrebug

@author: Andrew Kicklighter
"""

from PIL import Image, ImageDraw, ImageFont
from color import *
from name_fix import *
import sys
    

"""
Convert hex to RGBA
"""


def convert_to_rgb(hex):
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    rgb_str = ''
    for value in rgb:
        rgb_str = str(value) + ", " + rgb_str
    return rgb_str


"""
Recolor the team area to the team colors
"""


def recolor_team_area(img, home_color, away_color):
    home_hex = home_color.split("#")[1]
    away_hex = away_color.split("#")[1]

    home_rgb = convert_to_rgb(home_hex)
    away_rgb = convert_to_rgb(away_hex)

    img = img.convert('RGBA')
    pix_data = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            # If it is the default yellow
            if pix_data[x, y] == (231, 255, 27, 255):
                r = int(away_rgb.split(", ")[2])
                g = int(away_rgb.split(", ")[1])
                b = int(away_rgb.split(", ")[0])
                pix_data[x, y] = (r, g, b, 255)
            # If it is the default pink
            if pix_data[x, y] == (251, 0, 120, 255):
                r = int(home_rgb.split(", ")[2])
                g = int(home_rgb.split(", ")[1])
                b = int(home_rgb.split(", ")[0])
                pix_data[x, y] = (r, g, b, 255)

    return img


"""
Add team names to the score bug
"""


def add_team_names(img, home_team, away_team):
    home_team_len = len(home_team)
    away_team_len = len(away_team)

    draw = ImageDraw.Draw(img)

    if home_team_len >= 12:
        home_font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 30)
    elif home_team_len > 10:
        home_font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 34)
    else:
        home_font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 40)
    draw.text((753, 70), home_team, (255, 255, 255), anchor="ra", font=home_font)

    if away_team_len >= 12:
        away_font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 30)
    elif away_team_len > 10:
        away_font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 34)
    else:
        away_font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 40)
    draw.text((63, 70), away_team, (255, 255, 255), anchor="la", font=away_font)

    return img


"""
Add team names to the score bug
"""


def add_score(img, home_score, away_score):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 100)

    draw.text((421, 50), str(home_score), (255, 255, 255), anchor="la", font=font)
    draw.text((380, 50), str(away_score), (255, 255, 255), anchor="ra", font=font)

    return img


"""
Add possession to the score bug
"""


def add_possession(img, home_team, away_team, possession, home_score, away_score):
    draw = ImageDraw.Draw(img)
    if possession == home_team:
        if home_score < 10:
            draw.ellipse((496, 105, 506, 115), fill=(255, 255, 255, 255))
        elif 20 <= home_score < 30:
            draw.ellipse((539, 105, 549, 115), fill=(255, 255, 255, 255))
        elif home_score >= 30:
            draw.ellipse((535, 105, 545, 115), fill=(255, 255, 255, 255))
        else:
            draw.ellipse((520, 105, 530, 115), fill=(255, 255, 255, 255))
    elif possession == away_team:
        if away_score < 10:
            draw.ellipse((310, 105, 320, 115), fill=(255, 255, 255, 255))
        elif away_score < 20:
            draw.ellipse((277, 105, 287, 115), fill=(255, 255, 255, 255))
        else:
            draw.ellipse((260, 105, 270, 115), fill=(255, 255, 255, 255))

    return img


"""
Add quarter to the score bug
"""


def add_quarter(img, quarter):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 40)

    draw.text((67, 161), quarter, (255, 255, 255), font=font)

    return img


"""
Add clock to the score bug
"""


def add_clock(img, clock):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 40)

    draw.text((200, 161), clock, (255, 255, 255), font=font)

    return img


"""
Add down and distance to the score bug
"""


def add_down_and_distance(img, down_and_distance):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 40)

    draw.text((560, 161), down_and_distance, (255, 255, 255), font=font)

    return img


"""
Add team waiting on to the score bug
"""


def add_waiting_on(img, waiting_on):
    waiting_on = waiting_on.upper()
    waiting_on_len = len(waiting_on)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 20)

    if waiting_on_len > 10:
        shift = (waiting_on_len - 7) * 4
    elif waiting_on_len < 5:
        shift = (waiting_on_len - 7) * 1
    else:
        shift = (waiting_on_len - 7) * 3

    draw.text((350, 165), "WAITING ON", (255, 217, 0), font=font)
    draw.text((359-shift, 185), waiting_on, (255, 217, 0), font=font)

    return img


"""
Add odds to the score bug
"""


def add_odds(img, vegas_odds, team, home_team, away_team, shortened_home_team, shortened_away_team):
    if vegas_odds != "":
        vegas_odds = "(" + str(vegas_odds) + ")"

    home_team_len = len(shortened_home_team)
    away_team_len = len(shortened_away_team)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 25)

    if team == home_team:
        if home_team_len > 10:
            home_shift = (home_team_len - 7) * 4
        elif home_team_len < 5:
            home_shift = (home_team_len - 7) * 15
        else:
            home_shift = (home_team_len - 7) * 15
        draw.text((635-home_shift, 112), vegas_odds, (255, 255, 255), font=font)
    elif team == away_team:
        if away_team_len > 10:
            away_shift = (away_team_len - 10) * 6
        elif away_team_len < 5:
            away_shift = (away_team_len - 10) * -6
        else:
            away_shift = (away_team_len - 10) * -4
        draw.text((115-away_shift, 112), vegas_odds, (255, 255, 255), font=font)

    return img


"""
Add records to the score bug
"""


def add_records(img, home_record, away_record):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 30)
    home_wins = int(home_record.split("-")[0].split("(")[1])
    home_losses = int(home_record.split("-")[1].split(")")[0])

    draw.text((749, 118), home_record, (255, 255, 255), anchor="ra", font=font)
    draw.text((55, 118), away_record, (255, 255, 255), anchor="la", font=font)

    return img


"""
Add final to the score bug
"""


def add_final(img):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/home/ubuntu/FCFB/FCFB-Score-Bot/GazRg-BoldItalic.ttf", 40)

    draw.text((350, 161), "FINAL", (255, 217, 0), font=font)

    return img


"""
Draw the score bug
"""


def draw_scorebug(cur_clock, cur_down_and_distance, cur_possession, cur_yard_line, vegas_odds, home_team,
                  away_team, home_score, away_score, waiting_on, home_record, away_record):
    img = Image.open('/home/ubuntu/FCFB/FCFB-Score-Bot/scorebug.png')

    # Get team colors for plots
    color_dict = get_team_colors(home_team, away_team)
    if "The following error occurred:" not in color_dict:
        home_color = color_dict[1]
        away_color = color_dict[2]
        img = recolor_team_area(img, home_color, away_color)
        
        shortened_home_team = shorten_team_name(home_team)
        shortened_away_team = shorten_team_name(away_team)
        img = add_team_names(img, shortened_home_team, shortened_away_team)
        
        home_score = int(home_score)
        away_score = int(away_score)
        img = add_score(img, home_score, away_score)
        
        img = add_possession(img, home_team, away_team, cur_possession, home_score, away_score)

        quarter = cur_clock.split(" ")[1]
        if quarter == "1Q":
            quarter = "1st"
        elif quarter == "2Q":
            quarter = "2nd"
        elif quarter == "3Q":
            quarter = "3rd"
        elif quarter == "4Q":
            quarter = "4th"
        img = add_quarter(img, quarter)

        img = add_clock(img, cur_clock.split(" ")[0])

        img = add_down_and_distance(img, cur_down_and_distance)

        img = add_waiting_on(img, waiting_on)

        if home_record is not None and away_record is not None:
            img = add_records(img, home_record, away_record)

        # if home_score > away_score or home_score == away_score:
        #    img = add_odds(img, vegas_odds, home_team, home_team, away_team, shortened_home_team, shortened_away_team)
        # else:
        #    img = add_odds(img, vegas_odds, away_team, home_team, away_team, shortened_home_team, shortened_away_team)

        img.save('/home/ubuntu/FCFB/FCFB-Score-Bot/scorebug_new.png')
        
    else:
        print("Color retrieval error: " + color_dict)


"""
Draw the score bug
"""


def draw_final_scorebug(vegas_odds, home_team, away_team, home_score, away_score, home_record, away_record):
    img = Image.open('/home/ubuntu/FCFB/FCFB-Score-Bot/scorebug.png')

    # Get team colors for plots
    color_dict = get_team_colors(home_team, away_team)
    if "The following error occurred:" not in color_dict:
        home_color = color_dict[1]
        away_color = color_dict[2]
        img = recolor_team_area(img, home_color, away_color)

        shortened_home_team = shorten_team_name(home_team)
        shortened_away_team = shorten_team_name(away_team)
        img = add_team_names(img, shortened_home_team, shortened_away_team)

        home_score = int(home_score)
        away_score = int(away_score)
        img = add_score(img, home_score, away_score)

        img = add_final(img)

        if home_record is not None and away_record is not None:
            img = add_records(img, home_record, away_record)


        # if home_score > away_score or home_score == away_score:
        #    img = add_odds(img, vegas_odds, home_team, home_team, away_team, shortened_home_team, shortened_away_team)
        # else:
        #   img = add_odds(img, vegas_odds, away_team, home_team, away_team, shortened_home_team, shortened_away_team)

        img.save('/home/ubuntu/FCFB/FCFB-Score-Bot/scorebug_final.png')

    else:
        print("Color retrieval error: " + color_dict)
