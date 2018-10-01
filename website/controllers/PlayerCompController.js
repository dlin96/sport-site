var pg = require('pg');
var admin = require('./adminFuncs');

exports.playerStatGet = function(req, res) {
    client = connectToNflDb();
    console.log("GET /playercomp/");
    console.log("player1: " + req.query.player1);
    console.log("player2: " + req.query.player2);   

    // TODO: client-side input sanitization
    // TODO: think of a better way to cleanly end connection to db
    getPlayerStats(req.query.player1, function(result) {
        console.log("disconnecting...");
        client.end();
        return res.json(result);
    });
}

// TODO: use parameterized queries and change stats based on player position. 
playerIdQuery = "SELECT player_id, position FROM player WHERE full_name = ''";
statQuery = "SELECT SUM(passing_yds) as passing_yards, SUM(passing_tds) as tds, SUM(passing_cmp) * 100 / SUM(passing_att) as pass_pct FROM play_player as pp FULL OUTER JOIN game AS g ON pp.gsis_id = g.gsis_id WHERE player_id='00-0019596' AND g.season_type='Regular' AND g.season_year=2012 GROUP BY g.week";
function getPlayerStats(playerName, callback) {
    client.query("SELECT * from player where player_id='00-0019596'")
    .then(result => {
        console.log("full_name: " + result.rows[0].full_name);
        client.query(statQuery)
        .then(result => {
            callback(result);
        })
        .catch(e => console.log(e.stack));
    })
    .catch(e => console.error(e.stack));
};

// connect to nfldb 
function connectToNflDb() { 
    console.log("connectToNflDb");
    dbConfig = admin.loadConfig("db_conf.yaml");
    user = dbConfig["user"];
    password = dbConfig["password"];
    host = dbConfig["host"];
    database = dbConfig["database"];
    port = dbConfig["port"];

    const conString = {
        user: user,
        host: host,
        database: database,
        password: password,
        port: port,
    }

    const client = new pg.Client(conString);
    client.connect((err) => {
        if (err) {
            console.error('connection error', err.stack);
        } else {
            console.log ('connected');
        }
    });

    return client;
}