import nfldb

db = nfldb.connect()
q = nfldb.Query(db)

q.game(season_year=2015, season_type='Regular')
	
for pp in q.sort('defense_int').limit(64).as_aggregate():
	print pp.player, pp.defense_int