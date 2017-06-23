import urllib
import json
import MySQLdb

nba_stat_base_url = 'http://api.suredbits.com/nba/v0/stats'


def nba_roster_stats_population():
    # connect to MySQL db
    db = MySQLdb.connect(host="sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
                         user="root",
                         passwd="warriors73-9",
                         db="nbadb")
    # create Cursor object to execute queries
    cur = db.cursor()
    cur.execute();
    url = nba_stat_base_url + '/james/lebron'
    response = urllib.urlopen(url).read()
    stat_body = json.loads(response)
    print stat_body[0]['plusminus']

if __name__ == '__main__':
    nba_roster_stats_population()