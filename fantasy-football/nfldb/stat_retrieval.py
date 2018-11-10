#!/usr/bin/python

import urllib
import json
import pymysql
import configparser

nba_stat_base_url = 'http://data.nba.net/10s/prod/v1/data/10s/prod/v1/2016/players/%d_profile.json'

config = configparser.ConfigParser()
config.read("config.ini")
host = config.get("DatabaseInfo", "host")
user = config.get("DatabaseInfo", "user")
passwd = config.get("DatabaseInfo", "passwd")
db_name = config.get("DatabaseInfo", "db")

def config_file_test():
    db = pymysql.connect(host=host,
                         user=user,
                         passwd=passwd,
                         db=db_name)

    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute('''SELECT * FROM players WHERE lastName="Curry"''')
    row = cur.fetchone()
    print row

def nba_roster_stats_population():
    # connect to MySQL db
    db = pymysql.connect(host=host,
                         user=user,
                         passwd=passwd,
                         db=db_name)

    # create Cursor object to execute queries
    cur = db.cursor(pymysql.cursors.DictCursor)

    # select playerId from the players table
    cur.execute('''SELECT playerId FROM players''')
    player_id_list = []

    # populate the player name list for url
    for i in range(0, 445):
        row = cur.fetchone()
        pid = row['playerId']
        player_id_list.append(pid)

    for j in range(len(player_id_list)):
        pid = player_id_list[j]
        url = nba_stat_base_url % pid
        print url

        response = urllib.urlopen(url).read()
        stat_body = json.loads(response)

        '''
        apg, ast, blk, bpg, dd2, defreb, fga, fgm, fgp, fta, ftm, ftp, gp, gs, min, mpg, offreb, pfouls, plusminus, pts, 
        ppg, rpg, spg, st, td3, topg, totreb, tpa, tpm, tpp, to
        '''
        try:
            stat = stat_body['league']['standard']['stats']['regularSeason']['season'][0]['total']
            player_apg = stat['apg']
            player_ast = stat['assists']
            player_blk = stat['blocks']
            player_bpg = stat['bpg']
            player_dd2 = stat['dd2']
            player_defreb = stat['defReb']
            player_fga = stat['fga']
            player_fgm = stat['fgm']
            player_fgp = stat['fgp']
            player_fta = stat['fta']
            player_ftm = stat['ftm']
            player_ftp = stat['ftp']
            player_gp = stat['gamesPlayed']
            player_gs = stat['gamesStarted']
            player_min = stat['min']
            player_mpg = stat['mpg']
            player_offreb = stat['offReb']
            player_pfouls = stat['pFouls']
            player_plusminus = stat['plusMinus']
            player_pts = stat['points']
            player_ppg = stat['ppg']
            player_rpg = stat['rpg']
            player_spg = stat['spg']
            player_st = stat['steals']
            player_td3 = stat['td3']
            player_topg = stat['topg']
            player_totreb = stat['totReb']
            player_tpa = stat['tpa']
            player_tpm = stat['tpm']
            player_tpp = stat['tpp']
            player_to = stat['turnovers']
        except IndexError:
            continue

        cur.execute('''INSERT INTO stats (playerId, apg, ast, blk, bpg, dd2, defreb, fga, fgm, fgp, fta, ftm, ftp, gp, gs, min, mpg, offreb, pfouls, plusminus, pts, ppg, rpg, spg, st, td3, topg, totreb, tpa, tpm, tpp, tos)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (pid, player_apg, player_ast, player_blk, player_bpg, player_dd2, player_defreb, player_fga, player_fgm, player_fgp, player_fta, player_ftm, player_ftp, player_gp, player_gs, player_min, player_mpg, player_offreb, player_pfouls, player_plusminus, player_pts, player_ppg, player_rpg, player_spg, player_st, player_td3, player_topg, player_totreb, player_tpa, player_tpm, player_tpp, player_to))

        db.commit()
    db.close()

if __name__ == '__main__':
    # nba_roster_stats_population()
    config_file_test()