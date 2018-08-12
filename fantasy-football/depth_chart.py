import requests
import json
import mongodb_ops
import re
import logging
import bs4
import pickle


# logging config
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
dc_logger = logging.getLogger("dc_logger")
dc_logger.setLevel(logging.INFO)

team_dict = {}
position_list = ['WR ', 'LT ', 'LG ', 'C ', 'RG ', 'RT ', 'TE ', 'WR2 ', 'QB ', 'FB ', 'RB ']


def create_url(team_name):
    return "https://www.{}.com/team/depth-chart".format(team_name)


"""
function_name: create_depth_chart
purpose: gets the depth chart from the team website for a specified team
params: team_name - the name of the team to retrieve
return: dict containing positions as keys and a list of player names as values

TODO: Take care of edge cases like Will Fuller V or Joe Webb III. Perhaps
need to change scraping method. 
"""


def create_depth_chart(team_name):
    # opening URL and get response
    dc_logger.info("{}: {}".format(team_name, team_dict[team_name]))
    url = create_url(team_dict[team_name])
    response = requests.get(url)
    if response.status_code != 200:
        return None
    dc_logger.info("response: {}".format(response))
    soup = bs4.BeautifulSoup(response.text, "lxml")

    # use regular expressions to parse positions and get list of players
    player_table = re.sub("\s+", " ", soup.tbody.text).strip()
    pos_re = "[A-Z]{1,2}[0-9]?\s"
    name_re = "(\w+\s\w+)|(\w+\s\w+-\w+) | [A-Z].[A-Z].\s\w+"
    dc_logger.info("player_table: {}".format(player_table))
    pos = re.findall(pos_re, player_table)
    dc_logger.info("pos: {}".format(pos))
    names_list = re.split(pos_re, player_table)
    del(names_list[0])
    player_list = []
    for name in names_list:
        name_tups = re.findall(name_re, name.strip())
        # dc_logger.debug("name_tups: {}".format(name_tups))
        temp_list = [player_name for player in name_tups
                     for player_name in player if player_name]
        # dc_logger.debug("temp_list: {}".format(temp_list))
        player_list.append(temp_list)

    # return dictionary matching player lists and positions
    depth_chart = dict(zip(pos, player_list))
    dc_logger.info("test_list: {}".format(depth_chart))
    depth_chart["team_name"] = team_name
    return depth_chart


def create_team_list(json_file):
    with open(json_file, "rb") as file:
        global team_dict
        team_dict = json.load(file)
        dc_logger.info("team_dict: {}".format(team_dict))


def update_db():
    for team in team_dict.keys():
        dc = create_depth_chart(team)
        if dc is None:
            dc_logger.debug("URL failed to open")
            continue
        mongodb_ops.insert_dc(team, dc)


if __name__ == '__main__':
    create_team_list("teamnames.json")
    # update_db()
    create_depth_chart("texans")
