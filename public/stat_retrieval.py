import urllib
import json

nba_stat_base_url = 'http://api.suredbits.com/nba/v0/stats'


def nba_roster_stats_population():
    url = nba_stat_base_url + '/james/lebron'
    response = urllib.urlopen(url).read()
    stat_body = json.loads(response)
    print stat_body[0]['plusminus']

if __name__ == '__main__':
    nba_roster_stats_population()