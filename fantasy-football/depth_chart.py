import logging
import re
import requests
import traceback

import bs4

import mongodb_ops
import team_consts

# logging config
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
dc_logger = logging.getLogger("dc_logger")
dc_logger.setLevel(logging.INFO)


def create_depth_chart(team_name):

    """
    function_name: create_depth_chart
    purpose: gets the depth chart from the team website for a specified team
    params: team_name - the name of the team to retrieve
    return: dict containing positions as keys and a list of player names as values
    """

    # open URL and get response
    dc_logger.info("Team name: {}".format(team_name))
    url = team_consts.create_url(team_name, "team/depth-chart")

    dc_logger.info("URL: {}".format(url))
    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as exception:
        response = exception.response

        # page not found error
        if response.status_code == 404:
            dc_logger.error("URL not found! {}".format(url))
        else:
            dc_logger.error("Error requesting url! {}".format(url))
            raise

    dc_logger.info("response: {}".format(response.status_code))
    soup = bs4.BeautifulSoup(response.text, "lxml")

    # return dictionary matching player lists and positions
    try:
        depth_chart = make_player_dict(soup.tbody.text)
    except AttributeError:
        dc_logger.error("{} don't have depth chart available. Check again later.".format(team_name))
        return None

    # dc_logger.info("depth_chart: {}".format(depth_chart))
    depth_chart["team_name"] = team_name
    if depth_chart:
        insert_dc(team_name, depth_chart)
    return depth_chart


def make_player_dict(player_list):

    """
    function_name: make_player_dict
    purpose: create a player dict mapping the position to a list of player names (at that position, in order)
    params: @player_list: takes a string of positions followed by player names separated by newline characters
            "WR1\nPlayer1\nPlayer2\nWR2\n..."
    return: dictionary object containing position -> player_list mappings
    """

    value = ""
    name_list = []
    position = ""
    player_dict = {}

    try:
        table_body = re.sub(" +", " ", player_list.strip())
        player_list = re.sub("\n+", "\n", table_body)
        player_list = re.sub("\n \n", "\n", player_list)
    except AttributeError:
        traceback.print_exc()
        raise

    # iterate through each character in input string
    for c in player_list:

        # if we reached a newline character, we know we reached either the end of a name or position
        if c == '\n':

            # check if the value is a position or a player name
            pos_check = "".join(value.split())
            if pos_check in team_consts.POSITIONS:

                # check to see if this is the first position in the string
                if not position:
                    position = pos_check

                # if it's NOT the first position string encountered, and we have a non-empty list of players
                # then copy the list (otherwise its a reference to the same list), and then place it in dictionary
                if position and len(name_list) > 0:
                    if position in player_dict.keys():
                        position += "2"
                    player_dict[position] = name_list[:]
                    position = pos_check
                    name_list.clear()
            else:
                if value:       # avoid inserting empty string
                    name_list.append(value)
            value = ""
        elif c == '\r':
            continue
        else:
            value += c

    if position and len(name_list) > 0:
        if value:
            name_list.append(value)
        if position in player_dict.keys():
            position += "2"
        player_dict[position] = name_list[:]

    return player_dict


def insert_dc(collection_name, depth_chart_bson):

    """
    :function_name: insert_dc
    :param collection_name: team_name of depth chart
    :param depth_chart_bson: bson obj of depth chart
    :return: None
    """

    dc_logger.info("inserting into db")
    dc_logger.info("collection: {}".format(collection_name))
    dc_logger.info("dc_bson: {}".format(depth_chart_bson))
    _db, _connection = mongodb_ops.connect_db()
    collection = _db[collection_name]
    collection.replace_one({"team_name": collection_name}, depth_chart_bson, upsert=True)
    _connection.close()


if __name__ == '__main__':
    for team in team_consts.TEAM_NAMES:
        create_depth_chart(team)
