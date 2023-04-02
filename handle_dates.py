import datetime
import json

with open('/home/apkick/FCFB/FCFB-Score-Bot/season_information.json', 'r') as config_file:
    season_info_data = json.load(config_file)


"""
Parse a given month, day, year into a datetime date
"""


def parse_into_datetime(month, day, year):
    return datetime.datetime(year, month, day, 0, 0).date()


"""
Check if the gamethread is in the season
"""


def check_if_in_season(season, game_time):
    season_start_month = int(season_info_data['seasons'][season]['start_month'])
    season_start_day = int(season_info_data['seasons'][season]['start_day'])
    season_start_year = int(season_info_data['seasons'][season]['start_year'])
    season_start = parse_into_datetime(season_start_month, season_start_day, season_start_year)

    if season_info_data['seasons'][season]['end_month'] == "N/A":
        if season_start <= game_time.date():
            return True
        else:
            return False

    season_end_month = int(season_info_data['seasons'][season]['end_month'])
    season_end_day = int(season_info_data['seasons'][season]['end_day'])
    season_end_year = int(season_info_data['seasons'][season]['end_year'])
    season_end = parse_into_datetime(season_end_month, season_end_day, season_end_year)

    if season_start <= game_time.date() <= season_end:
        return True
    else:
        return False


"""
Check if the gamethread is in the postseason
"""


def check_if_in_postseason(season, game_time):
    if season_info_data['seasons'][season]['postseason_start_month'] == "N/A":
        return False

    postseason_start_month = int(season_info_data['seasons'][season]['postseason_start_month'])
    postseason_start_day = int(season_info_data['seasons'][season]['postseason_start_day'])
    postseason_start_year = int(season_info_data['seasons'][season]['postseason_start_year'])
    postseason_start = parse_into_datetime(postseason_start_month, postseason_start_day, postseason_start_year)

    season_end_month = int(season_info_data['seasons'][season]['end_month'])
    season_end_day = int(season_info_data['seasons'][season]['end_day'])
    season_end_year = int(season_info_data['seasons'][season]['end_year'])
    postseason_end = parse_into_datetime(season_end_month, season_end_day, season_end_year)

    if postseason_start <= game_time.date() <= postseason_end:
        return True
    else:
        return False



"""
Check if the gamethread is in the regularseason
"""


def check_if_in_regular_season(season, game_time):
    if season_info_data['seasons'][season]['postseason_start_month'] == "N/A":
        return True

    season_start_month = int(season_info_data['seasons'][season]['start_month'])
    season_start_day = int(season_info_data['seasons'][season]['start_day'])
    season_start_year = int(season_info_data['seasons'][season]['start_year'])
    season_start = parse_into_datetime(season_start_month, season_start_day, season_start_year)

    postseason_start_month = int(season_info_data['seasons'][season]['postseason_start_month'])
    postseason_start_day = int(season_info_data['seasons'][season]['postseason_start_day'])
    postseason_start_year = int(season_info_data['seasons'][season]['postseason_start_year'])
    postseason_start = parse_into_datetime(postseason_start_month, postseason_start_day, postseason_start_year)

    if season_start <= game_time.date() <= postseason_start:
        return True
    else:
        return False
