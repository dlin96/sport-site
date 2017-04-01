# Filename: info_retrieval.py
# Author: David Lin 
# Date: 3/30/17

import urllib
import json

nba_base_url = 'http://api.suredbits.com/nba/v0/players/'

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

def player_info_JSON(first_name, last_name):
	url = nba_base_url + lastname + '/' + first_name
	response = urllib.urlopen(url).read()
	data = json.loads(response)


