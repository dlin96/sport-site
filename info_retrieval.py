# Filename: info_retrieval.py
# Author: David Lin 
# Date: 3/30/17

import urllib, json, MySQLdb
import pprint as pp

# global variables
nba_base_url = 'http://api.suredbits.com/nba/v0/players'

"""
inputs: first_name, last_name
Correspond to the first and last names of the player we want to 
look up. 

purpose:
We want to parse the json object we get from the api call to 
suredbits. 

return:
JSON object of player (first_name, last_name) for use by another function.
JSON object of player information (not statistics).
E.g. height, weight, etc. 
"""


def player_info_json(first_name, last_name):
    url = nba_base_url + '/' + last_name + '/' + first_name
    response = urllib.urlopen(url).read()
    data = json.loads(response)
    pp.pprint(data)

"""
Inputs: none
Outputs: It will loop through the list of active players and insert them into the 
players database. 

Purpose: Populate our MySQL database with the active players in the roster. 
Variables: 
response - the body of the http response we get from the urllib call.
active_roster - array of json objects representing players in the NBA. 
"""


def populate_nba_players():
    # connect to MySQL db
    db = MySQLdb.connect(host="sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
                         user="root",
                         passwd="warriors73-9",
                         db="nbadb")
    # create Cursor object to execute queries
    cur = db.cursor()
    response = urllib.urlopen(nba_base_url).read()
    active_roster = json.loads(response)
    for player in active_roster:
        player_ln = player['lastName']
        player_fn = player['firstName']
        player_full = player['fullName']

        # TODO: Find a more elegant solution here
        if 'height' not in player:
            player_height = '0-0'
        else:
            player_height = player['height']
        if 'weight' not in player:
            player_weight = 0
        else:
            player_weight = player['weight']
        player_profileURL = player['profileUrl']
        player_team = player['team']
        if 'position' not in player:
            player_position = 'Empty'
        else:
            player_position = player['position']
        player_playerId = player['playerId']
        player_status = player['status']
        if 'uniformNumber' not in player:
            player_number = 0
        else:
            player_number = player['uniformNumber']
        cur.execute('''INSERT INTO players (lastName, firstName, fullName, height, weight, profileURL, team, position, playerId, status, number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (player_ln, player_fn, player_full, player_height, player_weight, player_profileURL, player_team, player_position, player_playerId, player_status, player_number))

        db.commit()
    db.close()

'''
Inputs: The columns of the players db (some of which will be optional).
Purpose: Insert a specific player into the players database that might not be in the current DB. 

Description: Should take all the necessary fields of a "player" in the table and insert it. 
'''

# TODO: Make height, weight, position optional parameters
# def insert_player(last_name, first_name, full_name, height, weight, profileURL, team, position, playerId, status, number):


# if the program is being run as standalone
if __name__ == '__main__':
    populate_nba_players()
