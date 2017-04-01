import urllib
import json

nba_base_url = 'http://api.suredbits.com/nba/v0/players/'

def spec_player_JSON(first_name, last_name):
	url = nba_base_url + lastname + '/' + first_name
	response = urllib.urlopen(url).read()
