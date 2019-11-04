import logging
import requests
import re
import time

from bs4 import BeautifulSoup

import mongodb_ops
import team_consts

FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
sched_logger = logging.getLogger("sched_logger")
sched_logger.setLevel(logging.INFO)


def scrape_schedule(teamname):
    matchups = "nfl-o-matchup-cards"
    # weeks = "nfl-o-matchup-cards__date-info"
    opponent = "nfl-o-matchup-cards__team-full-name"
    season_type = "d3-o-section-title"
    team_sched = []

    sched_logger.info("teamname: {}".format(teamname))
    url = team_consts.create_url(teamname, "schedule")
    sched_logger.info("url: {}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        pre_reg = soup.find_all(class_=season_type)
        seas_types = []
        for item in pre_reg:
            span = item.find("span")
            if span:
                text = span.text.strip()
                if text == "REGULAR SEASON" or text == "PRESEASON":
                    seas_types.append(text)

        sched_logger.info(seas_types)
        schedule = soup.find_all(class_=matchups)
        for item in schedule:
            # week = item.find_all(class_=weeks)[0].find("strong").text.strip()
            opp = "BYE"
            if len(item.find_all(class_=opponent)) > 0:
                opp = item.find_all(class_=opponent)[0].text.strip()
            # week = re.match(".*\\s([0-9]+)", week).group(1)
            team_sched.append(opp)

        if seas_types[0] == "PRESEASON":
            return team_sched[-17:]
        else:
            return team_sched[:17]
    else:
        sched_logger.error("STATUS CODE: {}".format(response.status_code))
        sched_logger.error("Try again later for team: {}".format(teamname))


def insert_sched(schedule_bson):

    """
    :function_name: insert_sched
    :param schedule_bson: bson obj of team's schedule
    :return: None
    """

    collection_name = "schedules"
    sched_logger.info("inserting schedule for team: {}".format(collection_name))
    _db, _connection = mongodb_ops.connect_db()
    collection = _db[collection_name]
    collection.replace_one({"team_name": collection_name}, schedule_bson, upsert=True)
    _connection.close()


def update_scheds():
    sched_dict = {}
    for team_name in team_consts.TEAM_NAMES:
        sched_dict[team_name] = scrape_schedule(team_name)
        time.sleep(2)
    insert_sched(sched_dict)


if __name__ == "__main__":
    update_scheds()
    # sched_logger.info(scrape_schedule("patriots"))
