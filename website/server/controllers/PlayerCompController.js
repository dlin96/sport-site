const {Pool, Client} = require('pg');
const admin = require('./adminFuncs');

const config = connectToNflDb();
const pool = new Pool(config);

exports.playerStatGet = function(req, res, next) {
    console.log("GET /playercomp/");
    console.log("player1: " + req.query.player1);
    console.log("player2: " + req.query.player2);  
    console.log("year: " + req.query.year); 

    if(req.query.player1 == undefined || req.query.player2 == undefined) {
        return;
    }

    let retArr = [];
    // TODO: modify this to queue up promises instead of doing it sequentially
    getPlayerStats(req.query.player1, req.query.year, function(result) {
        // console.log(result);
        if(!Object.keys(result).length) res.send(result);
        retArr.push(result.rows[0]);
        getPlayerStats(req.query.player2, req.query.year, function(result) {
            result["player_name"] = req.query.player2;
            retArr.push(result.rows[0]);
            console.log(retArr);
            // pool.end();
            res.render("pages/index", {player1: retArr[0], player2: retArr[1]});
        });
    });
    
}

// TODO: column and table names must be literals - limitation of PGSQL. Use client-side JS to generate query. 
const playerIdQuery = "SELECT player_id, position, full_name FROM player WHERE lower(full_name) = $1";
const statQuery = 
"SELECT SUM(passing_yds) as passing_yds, SUM(passing_tds) as passing_tds, SUM(passing_att) as passing_att, \
CASE WHEN SUM(passing_att) = 0 THEN 0 ELSE SUM(passing_cmp) * 100 / SUM(passing_att) \
end as pass_pct, SUM(rushing_yds) as rushing_yds, SUM(rushing_att) as rushing_att, CASE WHEN SUM(rushing_att) = 0 THEN 0 ELSE SUM(rushing_yds)/SUM(rushing_att) end as ypc, \
SUM(rushing_tds) as rushing_tds, SUM(receiving_yds) as receiving_yds, \
SUM(receiving_tds) as receiving_tds, SUM(receiving_tar) as receiving_tar, SUM(receiving_yac_yds) as receiving_yac_yds, \
SUM(receiving_rec) as receiving_rec FROM play_player as pp FULL OUTER JOIN game AS g ON pp.gsis_id = g.gsis_id \
WHERE player_id=$1 AND g.season_type='Regular' AND g.season_year=$2";

// const avgWR = "";

function getPlayerStats(playerName, year, callback) {
    pool.query(playerIdQuery, [playerName.toLowerCase()])
    .then(result => {
        console.log("rows: " + result['rows']);
        if(!result['rows'].length) {
            console.error("empty rows!!")
            callback(result);
            return;
        }
        console.log("full_name: " + result.rows[0].full_name);
        console.log("position: " + result.rows[0].position);
        pool.query(statQuery, [result.rows[0].player_id, year])
        .then(result => {
            result.rows[0]["player_name"] = playerName;
            callback(result);
        })
        .catch(e => console.log(e.stack));
    })
    .catch(e => {
        console.error(e.stack)
        pool.end();
    })
};

exports.autocompleteSearch = function(req, res) {
    console.log("connecting to nfldb...");
    _client = connectToNflDb();

    console.log("params:");
    console.log(req.query.playername);

    // query for players with similar names
    playerIdQuery = 'SELECT full_name FROM player WHERE lower(full_name) like $1';
    _client.query(playerIdQuery, [req.query.playername+"%"])
        .then(response => {
            console.log(response);
            res.json(response.rows);
        })
        .catch(e => {
            console.log(e);
            _client.end();
        });
}

// connect to nfldb 
function connectToNflDb() { 
    console.log("connectToNflDb");
    dbConfig = admin.loadConfig("./db_conf.yaml");
    user = dbConfig["user"];
    password = dbConfig["password"];
    host = dbConfig["host"];
    database = dbConfig["database"];
    port = dbConfig["port"];

    const config = {
        user: user,
        host: host,
        database: database,
        password: password,
        port: port,
    }

    return config;
}
