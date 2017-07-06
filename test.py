import urllib
import json
import pprint

test_url = "http://data.nba.net/10s/prod/v1/data/10s/prod/v1/2016/players/1627732_profile.json"

def curry_stats():
	response = urllib.urlopen(test_url).read()
	stat_body = json.loads(response)

	pprint.pprint(stat_body['league']['standard']['stats']['regularSeason']['season'][0]['total']['apg'])
	# pprint.pprint(stat_body)

if __name__ == '__main__':
	curry_stats()