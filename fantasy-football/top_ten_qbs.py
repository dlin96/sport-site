import nfldb

db = nfldb.connect()
q = nfldb.Query(db)

q.game(season_year=2012, season_type="Regular", week=1)
q.player(full_name="Tom Brady").play(passing_tds__ge=1)
for p in q.as_plays():
    print p
