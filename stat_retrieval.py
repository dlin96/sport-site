import urllib
import json
import pymysql

nba_stat_base_url = 'http://api.suredbits.com/nba/v0/stats'


def nba_roster_stats_population():
    # connect to MySQL db
    db = pymysql.connect(host="sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
                         user="root",
                         passwd="warriors73-9",
                         db="nbadb")
    # create Cursor object to execute queries
    cur = db.cursor(pymysql.cursors.DictCursor)
    cur.execute('''SELECT fullName FROM players ORDER BY lastName''')
    player_list = []

    # populate the player name list for url
    for i in range(0, 445):
        row = cur.fetchone()
        fullName = row['fullName']
        player_list.append(fullName)

    # fetch all players in the db
    for j in range(0, 445): # TODO: don't use magic numbers here
        name = player_list[j].split()
        fname = name[0].lower()
        lname = name[1].lower()

        if ',' in lname:
            temp = lname.split(',')
            lname = temp[0]
            
        url = nba_stat_base_url + '/' + lname + '/' + fname
        print url
        response = urllib.urlopen(url).read()
        stat_body = json.loads(response)
        if len(stat_body) > 0:
            stats = stat_body[0]
            # # st, fta, bs, off, pf, min, fgm, tos, def, pts, tpa, playerId, ftm, fga, plusminus, ast, tpm, tot
            player_st = stat_body[0]['st']
            player_fta = stat_body[0]['fta']
            player_bs = stat_body[0]['bs']
            player_off = stat_body[0]['off']
            player_pf = stat_body[0]['pf']
            player_min = stat_body[0]['min']
            player_fgm = stat_body[0]['fgm']
            player_tos = stat_body[0]['to']
            player_def = stat_body[0]['deff']
            player_pts = stat_body[0]['pts']
            player_tpa = stat_body[0]['tpa']
            player_playerId = stat_body[0]['playerId']
            player_ftm = stat_body[0]['ftm']
            player_fga = stat_body[0]['fga']
            player_plusminus = stat_body[0]['plusminus']
            player_ast = stat_body[0]['ast']
            player_tpm = stat_body[0]['tpm']
            player_tot = stat_body[0]['tot']

            cur.execute('''INSERT INTO stats (st, fta, bs, offreb, pf, min, fgm, tos, defreb, pts, tpa, playerId, ftm, fga, plusminus, ast, tpm, totreb)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                        (player_st, player_fta, player_bs, player_off, player_pf, player_min, player_fgm, player_tos, player_def, player_pts, player_tpa, player_playerId,
                            player_ftm, player_fga, player_plusminus, player_ast, player_tpm, player_tot))

            db.commit()
    db.close()

if __name__ == '__main__':
    nba_roster_stats_population()