from multiprocessing.dummy import Pool
import pickle
import traceback
import timeit
import re
import requests
import logging
import bs4
import tqdm
import redis
import mongodb_ops

# logging config
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(format=FORMAT)
dc_logger = logging.getLogger("dc_logger")
dc_logger.setLevel(logging.INFO)

team_names = \
    ('texans', 'titans', 'colts', 'jaguars',                    # AFC South
           'ravens', 'browns', 'bengals', 'steelers',           # AFC North
           'raiders', 'chiefs', 'chargers', 'broncos',          # AFC West
           'patriots', 'dolphins', 'bills', 'jets',             # AFC East
           'cowboys', 'eagles', 'redskins', 'giants',           # NFC East
           'bears', 'lions', 'packers', 'vikings',              # NFC North
           'falcons', 'saints', 'panthers', 'buccaneers',       # NFC South
           'seahawks', 'niners', 'rams', 'cardinals')           # NFC West

exception_dict = {
    "texans": "houstontexans",
    "titans": "titansonline",
    "ravens": "baltimoreravens",
    "browns": "clevelandbrowns",
    "broncos": "denverbroncos",
    "dolphins": "miamidolphins",
    "bills": "buffalobills",
    "jets": "newyorkjets",
    "cowboys": "dallascowboys",
    "eagles": "philadelphiaeagles",
    "bears": "chicagobears",
    "lions": "detroitlions",
    "falcons": "atlantafalcons",
    "saints": "neworleanssaints",
    "niners": "49ers",
    "rams": "therams",
    "cardinals": "azcardinals"
}
position_list = ('WR ', 'LT ', 'LG ', 'C ', 'RG ', 'RT ', 'TE ', 'WR2 ', 'QB ',
                 'FB ', 'RB ')


def create_url(team_name):
    if team_name in exception_dict:
        team_name = exception_dict[team_name]
    return "https://www.{}.com/team/depth-chart".format(team_name)


"""
function_name: create_depth_chart
purpose: gets the depth chart from the team website for a specified team
params: team_name - the name of the team to retrieve
return: dict containing positions as keys and a list of player names as values
"""


def create_depth_chart(team_name):

    # open URL and get response
    dc_logger.info("Team name: {}".format(team_name))
    url = create_url(team_name)

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

    # use regular expressions to parse positions and get list of players
    """
    try:
        table_body = re.sub(" +", " ", soup.tbody.text.strip())
        player_table = re.sub("\n+", "\n", table_body)
        player_table = re.sub("\n \n", "\n", player_table)

        dc_logger.debug("{}".format(player_table))
    except AttributeError:
        traceback.print_exc()
        dc_logger.error("{} don't have depth chart available. Check again later.".format(team_name))
        return None
    """

    # return dictionary matching player lists and positions
    try:
        depth_chart = make_player_dict(soup.tbody.text)
    except AttributeError:
        dc_logger.error("{} don't have depth chart available. Check again later.".format(team_name))
        return None

    # dc_logger.info("depth_chart: {}".format(depth_chart))
    depth_chart["team_name"] = team_name
    if depth_chart:
        mongodb_ops.insert_dc(team_name, depth_chart)
    return depth_chart


"""
function_name: make_player_dict
purpose: create a player dict mapping the position to a list of player names (at that position, in order)
params: @player_list: takes a string of positions followed by player names separated by newline characters
        "WR1\nPlayer1\nPlayer2\nWR2\n..." 
return: dictionary object containing position -> player_list mappings
"""


def make_player_dict(player_list):
    positions = ('WR', 'LWR', 'RWR', 'WR1', 'WR2', 'LT', 'LG', 'C', 'RG', 'RT', 'TE', 'QB', 'RB', 'SE', 'FL', 'FB')

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
            if pos_check in positions:

                # check to see if this is the first position in the string
                if not position:
                    position = pos_check

                # if it's NOT the first position string encountered, and we have a non-empty list of players
                # then copy the list (otherwise its a reference to the same list), and then place it in dictionary
                if position and len(name_list) > 0:
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
        player_dict[position] = name_list[:]

    return player_dict


def mt_update():
    with Pool(4) as p:
        list(tqdm.tqdm(p.imap(create_depth_chart, team_names), total=len(team_names)))


if __name__ == '__main__':
    # print(timeit.timeit("mt_update()", 'from __main__ import mt_update'))
    mt_update()
    # p_dict = create_depth_chart("ravens")
    # with open("./tests/ravens_2018.pkl", "wb") as file:
    #    pickle.dump(p_dict, file)
