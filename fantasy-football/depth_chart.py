import requests
import json
import re
import pprint
import logging
import pickle
import os
import yaml
from pymongo import MongoClient

# String Values to access fields of JSON object
players = "players"
json_extension = "json"
text_extension = "txt"
player_dict = {}
team_dict = {}
exception_dict = {}
dc = {}

with open ("mongoconf.yaml", "r") as conf:
    doc = yaml.load(conf)
    username = doc["username"]
    password = doc["password"]

# connect to MongoDB instance
connection = MongoClient('localhost',
                         27017,
                         username=username,
                         password=password,
                         authSource="admin",
                         )
db = connection['fantasy-football-db']


def insert_team_list():
    collection = db['teams']
    collection.save(team_dict)
    db.collection_names(include_system_collections=False)
    pprint.pprint(collection.find_one())


def insert_dc(team_name):
    print("dict: {}".format(db[team_name]))
    collection = db[team_name]
    print("Dc: {}".format(type(dc)))
    dc.update({"team_name": team_name})
    collection.update({"team_name": team_name}, document=dict(dc), upsert=True)
    db.collection_names(include_system_collections=False)
    logging.debug("{} : {}".format(collection, collection.find_one()))


def populate_teams_dict():
    # check if pickle file exists
    if os.path.isfile("team_dict.pickle"):
        with open("team_dict.pickle", "rb") as file:
            global team_dict
            team_dict=pickle.load(file)
    else:
        populate_teams_dict_pickle()


# This method populates the team dictionary with the team name as the key and the URL version of team name as value
def populate_teams_dict_pickle():
    with open("teamnames.txt", 'r') as team_names:
        for team in team_names:
            logging.info("team_key: " + team)
            val = team_names.readline()
            key = team.rstrip('\n')
            value = val.rstrip('\n')
            team_dict[key] = value
    with open("team_dict.pickle", "wb") as file:
        pickle.dump(team_dict,file, pickle.DEFAULT_PROTOCOL)


def populate_exception_dict():
    # check if pickle file exists
    if os.path.isfile("exception_dict.pickle"):
        with open("exception_dict.pickle", "rb") as file:
            global exception_dict
            exception_dict=pickle.load(file)
    else:
        populate_exception_dict_pickle()


# populate the dictionaries containing the teams that don't use JSON objects for depth charts
def populate_exception_dict_pickle():
    with open("exception_teams.txt", 'r') as without_json:
        for team_key in without_json:
            val = without_json.readline()
            key = team_key.rstrip('\n')
            value = val.rstrip('\n')
            exception_dict[key] = value

    with open("exception_dict.pickle", "wb") as file:
        pickle.dump(exception_dict, file, pickle.DEFAULT_PROTOCOL)


def create_url(team_name):
    depth_chart_url_tail = "depth-chart"
    url = "http://www." + team_dict[team_name]
    url += ".com/team/" + depth_chart_url_tail + ".html"
    return url


# create the file name based on the file type. I.e. Files containing JSON objects go into JSON folder.
def create_file_name(team_name, extension):
    file_name_tail = "_DepthChart."
    json_path = "JSON_files/"

    file_name = json_path + team_name + file_name_tail + extension
    return file_name


# get the depth chart from JSON objects.
def get_depth_chart_json(team_name):
    url = create_url(team_name)
    response = requests.get(url)
    data = response.text
    latter_half = re.split("depthChartJson = ", data)
    if len(latter_half) > 1:
        json_object = re.split("</script>", latter_half[1])
        depth_chart = json_object[0]
    else: return False

    # write JSON object to file
    with open(create_file_name(team_name, json_extension), "w+") as log_file:
        log_file.write(depth_chart)

    return True


# set the player dictionary for the team name.
def set_player_dict(team_name):

    with open(create_file_name(team_name, json_extension)) as json_data:    # open team JSON file
        data = json.load(json_data)

    for index in range(len(data[players])):	    # go through player list and get name
        player_name = data[players][index]["fname"] + " " + data[players][index]["lname"]

        # store player names under their ID value
        player_id = data[players][index]["id"]
        player_dict[player_id] = player_name

    return data


# get the starters of the team. 
# TODO: rename this. This function no longer gets the starters
def get_starters(team_name):

    dc.clear()
    data = set_player_dict(team_name)

# get offense players from JSON. Write depth chart to file.
    for index in range(len(data["formations"]["Offense"]["Base"])):

        # position
        position = data["formations"]["Offense"]["Base"][index]["positionID"]
        if "1" in position:
            position = position.strip("1")
        if position in dc.keys():
            position += "2"
        player_list = []

        for i in range(len(data["formations"]["Offense"]["Base"][index][players])):
            # player names
            player_list.append(player_dict[data["formations"]["Offense"]["Base"][index][players][i]])

        dc[position] = dc.get(position, []) + player_list

    # no support for defense yet
    # for index in range(len(data[formations]["Defense"]["Base"])):
    #     position = data[formations]["Defense"]["Base"][index]["positionId"]
    #     player_list = []

    #     for i in range(len(data[formations]["Defense"]["Base"][index][players])):
    #         player_list.append(player_dict[data[formations]["Defense"]["Base"][index][players][i]])
    #         dc[position] = player_list


# update depth charts
def update_db():
    populate()
    for team in team_dict:
        print(team)
        if not get_depth_chart_json(team):
            continue
        set_player_dict(team)
        get_starters(team)
        insert_dc(team)
    connection.close()


def main(team_name):
    if team_name not in team_dict:
        print("Not a valid team name.")
        return

    get_depth_chart_json(team_name)
    set_player_dict(team_name)
    get_starters(team_name)
    insert_dc(team_name)
    connection.close()


def populate():
    populate_teams_dict()
    populate_exception_dict()