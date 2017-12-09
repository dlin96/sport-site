var http = require('http');
var mysql = require('mysql');
var prompt = require('prompt');
var express = require('express');
var bodyParser = require('body-parser');
var iniParser = require('ini');
var fs = require('fs');
var cors = require('cors');

var app = express();

app.set('views',__dirname + '/src');
app.use(express.static(__dirname + '/js'));
app.use(express.static('src'))
app.use(cors({
	origin: 'http://localhost:3000'
}));
app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true}));
app.engine('html', require('ejs').renderFile);

// function to connect to mysqldb. Created for sake of reusability. 
function dbConnection() {
	var config = iniParser.parse(fs.readFileSync('../config.ini', 'utf-8'));

	// create mysql connection 
	var con = mysql.createConnection({
		host: config.DatabaseInfo.host,
		user: config.DatabaseInfo.user,
		password: config.DatabaseInfo.passwd,
		database: config.DatabaseInfo.db
	});

	// connect to the db
	con.connect();
	return con;
}

// app.get('/', function(req, res) {

// 	res.sendFile(__dirname + '/src/index.html');
// });

app.get('/search', function(req, res) {
	var con = dbConnection();
	// query using the user input
	var query = 'SELECT fullName, playerId, team FROM players WHERE fullName LIKE "%' + req.query.key+'%"';
	con.query(query, function(err, rows, fields) {
		var data=[];
		for(var i=0; i<rows.length;i++) {
			data.push(rows[i].fullName + " " + rows[i].team);
		}

		json = JSON.stringify(data);
		res.send(json);
	});
});

function splitParam(url_param) {
	var fullName = url_param;
	var playerNameArr = fullName.split(' ');
	fullName = playerNameArr[0] + ' ' + playerNameArr[1];
	var team = playerNameArr[2]; 

	return [fullName, team];
}

/*
 * Post method that takes the input from the page and returns a json of the 
 * selected players stats. This method is strictly for comparing 2 players.
 *
 * TODO: see if we can avoid doing a query for playerId. Modify queries to 
 *		 escape '' against SQL injection
 */

app.get('/comparison/', function(req, res) {
	var con = dbConnection();
	var playerOne = splitParam(req.query.player);
	var fullName = playerOne[0];
	var team = playerOne[1];

	var playerTwo = splitParam(req.query.player2);
	var fullName2 = playerTwo[0];
	var team2 = playerTwo[1];

	//retrieves playerId from the fullName and team. 
	var q =  'SELECT playerId FROM players WHERE fullName="' + fullName2 + '" AND team="' + team2 +'"';
	var query = 'SELECT playerId FROM players WHERE fullName="'+fullName+'" AND team="'+team+'" UNION ' + q;
	con.query(query, function(err, rows, fields) {
		if(rows[0] && rows[1]) {
			var playerId = rows[0].playerId;
			var playerId2 = rows[1].playerId;

			// retrieves the stats from the given unique playerId.
			var secQ = 'SELECT * FROM stats WHERE playerId="'+playerId2+'"'
			var secQuery = 'SELECT * FROM stats WHERE playerId="'+playerId+'" UNION ' + secQ;
			con.query(secQuery, function(err, rows) {
				var json = JSON.stringify([rows[0], rows[1]]);
				// console.log(json);
				res.send(json);
			});
		} else {
			var json = {};
			res.send(json);
		}
	});
});

app.get('/json/:playername', function (req, res) {
	var playername = req.params.playername;

	var con = dbConnection();
	
	//retrieve playerId
	var playerIDquery = 'SELECT playerId FROM players WHERE fullname LIKE "%' + playername +'%"';
	con.query(playerIDquery, function(err, rows, fields) {

		//data should only contain one player id
		var playerID = rows[0].playerId;

		var statsQuery = 'SELECT * FROM stats WHERE playerId LIKE "%' + playerID + '%"';

		con.query(statsQuery, function(_err, _rows, _fields) {

			var data = _rows[0];
			var json = JSON.stringify(data);

			console.log(json);
			res.end(json);

			con.end(); 
		});
	});
});

// app.get('/compare', function(req, res) {
// 	res.sendFile(__dirname + '/public/player_comp.html');
// })

// start our server, listening on port 3000
var server=app.listen(8000,function(){
	console.log("We have started our server on port 8000");
});
