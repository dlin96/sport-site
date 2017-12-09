#!/usr/bin/python

# Filename: info_retrieval.py
# Author: David Lin 
# Date: 3/30/17

import urllib
import json
import MySQLdb
import pprint as pp
import configparser

# global variables
nba_base_url = 'http://api.suredbits.com/nba/v0/players'
config = configparser.ConfigParser()
config.read("config.ini")
host = config.get("DatabaseInfo", "host")
user = config.get("DatabaseInfo", "user")
passwd = config.get("DatabaseInfo", "passwd")
db_name = config.get("DatabaseInfo", "db")

class nba_db:


    '''
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
    '''


    def player_info_json(self, first_name, last_name):
        url = nba_base_url + '/' + last_name + '/' + first_name
        response = urllib.urlopen(url).read()
        data = json.loads(response)
        pp.pprint(data)

    '''
    Inputs: none
    Outputs: It will loop through the list of active players and insert them into the 
    players database. 

    Purpose: Populate our MySQL database with the active players in the roster. DOES NOT GET STATS.
    Variables: 
    response - the body of the http response we get from the urllib call.
    active_roster - array of json objects representing players in the NBA. 
    '''


    def populate_nba_players(self):
        # connect to MySQL db
        db = MySQLdb.connect(host=host,
                            user=user,
                            passwd=passwd,
                            db=db_name)
        # create Cursor object to execute queries
        cur = db.cursor()

        # get the JSON of players
        response = urllib.urlopen(nba_base_url).read()
        active_roster = json.loads(response)

        # loop through each player in the active roster
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

    Description: Should take all the necessary fields of a "player" in the table and insert it. DOES NOT GET STATS
    '''


    # TODO: NEEDS TESTING.
    def insert_player(self, last_name, first_name, playerId):
        # connect to MySQL db
        db = MySQLdb.connect(host=host,
                            user=user,
                            passwd=passwd,
                            db=db_name)
        # create Cursor object to execute queries
        cur = db.cursor()
        url = nba_base_url + '/' + last_name + '/' + first_name
        response = urllib.urlopen(url).read()
        player = json.loads(response)
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
        player_profile_url = player['profileUrl']
        player_team = player['team']
        if 'position' not in player:
            player_position = 'Empty'
        else:
            player_position = player['position']
        player_player_id = player['playerId']
        player_status = player['status']
        if 'uniformNumber' not in player:
            player_number = 0
        else:
            player_number = player['uniformNumber']
        cur.execute('''INSERT INTO players (lastName, firstName, fullName, height, weight, profileURL, team, position, playerId, status, number)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                    (player_ln, player_fn, player_full, player_height, player_weight, player_profile_url, player_team,
                    player_position, player_player_id, player_status, player_number))
        db.commit()
        db.close()

# NFL Player Info Retrieval will go here

# if the program is being run as standalone
if __name__ == '__main__':
    nba = nba_db()
    nba.player_info_json("Stephen", "Curry") 