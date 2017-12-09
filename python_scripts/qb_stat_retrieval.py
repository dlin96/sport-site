#!/usr/bin/python

import nfldb

db = nfldb.connect()

games = []

'''
At first, this will get only Tom Brady stats (for the sake of my report). 
Afterwards, I will modify it to make it for any team and any season type. 
'''

def get_reg_season():
	f = open('games_list_09', 'w')

	q = nfldb.Query(db).game(season_type='Regular', team='NE')
	q.game(season_year=[2009])
	q.sort('week')
	for game in q.as_games():
		f.write(str(game) + '\n')
		games.append(game)

	f.close()


def get_drives(game):
	f = open('' + str(game.season_year) + '_' + str(game.week)+ '_' + 'drive_list', 'w')
	f.write(str(game))
	for drive in game.drives:
		f.write(str(drive) + '\n')

	f.close()



get_reg_season()
get_drives(games[0])