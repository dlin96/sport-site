var http = require('http');
var mysql = require('mysql');
var prompt = require('prompt');
var express = require('express');
var bodyParser = require('body-parser');

var app = express();

app.set('views',__dirname + '/public');
app.use(express.static(__dirname + '/js'));
app.set('view engine', 'ejs');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true}));
app.engine('html', require('ejs').renderFile);

// function to connect to mysqldb. Created for sake of reusability. 
// create mysql connection 
var con = mysql.createConnection({
	host: "sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
	user: "root",
	password: "warriors73-9",
	database: "nbadb"
});

// connect to the db
con.connect();

app.get('/', function(req, res) {
	res.sendFile(__dirname + '/public/index.html');
});

app.get('/search', function(req, res) {
	// dbConnection();
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
	var playerNameArr = fullName.split();
	fullName = playerNameArr[0] + ' ' + playerNameArr[1];
	var team = playerNameArr[2]; 

	return [fullName, team];
}

/*
 * Post method that takes the input from the page and returns a json of the 
 * selected players stats. This method is strictly for comparing 2 players.
 *
 * TODO: see if we can avoid doing a query for playerId.
 *		 need to refactor the duplicate code for both players
 */

app.post('/comparison/:playerName/:player2', function(req, res) {

	// dbConnection();
	// player 1
	var fullName = req.params.playerName;
	var playerNameArr = fullName.split(' ');
	fullName = playerNameArr[0] + ' ' + playerNameArr[1];
	var team = playerNameArr[2]; 

	// player 2
	var fullName2 = req.params.player2;
	var playerNameArr2 = fullName2.split(' ');
	fullName2 = playerNameArr2[0] + ' ' + playerNameArr2[1];
	var team2 = playerNameArr2[2]; 


	// var data = splitParam(req.params.playerName);
	// console.log(data);
	// var fullName = data[0];
	// var team = data[1];

	//retrieves playerId from the fullName and team. 
	var q =  'SELECT playerId FROM players WHERE fullName="' + fullName2 + '" AND team="' + team2 +'"';
	var query = 'SELECT playerId FROM players WHERE fullName="'+fullName+'" AND team="'+team+'" UNION ' + q;
	con.query(query, function(err, rows, fields) {
		var playerId = rows[0].playerId;
		var playerId2 = rows[1].playerId;

		// retrieves the stats from the given unique playerId.
		var secQ = 'SELECT * FROM stats WHERE playerId="'+playerId2+'"'
		var secQuery = 'SELECT * FROM stats WHERE playerId="'+playerId+'" UNION ' + secQ;
		con.query(secQuery, function(err, rows) {
			console.log(rows[0]);
			console.log(rows[1]);
			var json = JSON.stringify([rows[0], rows[1]]);
			res.send(json);
		});
	});
});

app.get('/json/:playername', function (req, res) {
	var playername = req.params.playername;
	// create mysql connection
	var con = mysql.createConnection({
		host: "sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
		user: "root",
		password: "warriors73-9",
		database: "nbadb"
	});

	//connect to db
	con.connect();
	
	//retrieve playerId
	var playerIDquery = 'SELECT playerId FROM players WHERE fullname LIKE "%' + playername +'%"';
	con.query(playerIDquery, function(err, rows, fields) {
		//data should only contain one player Id
		var playerID = rows[0].playerId;

		var statsQuery = 'SELECT pts, ast, tpm FROM stats WHERE playerId LIKE "%' + playerID + '%"';

		con.query(statsQuery, function(_err, _rows, _fields) {
			res.json(_rows);
			console.log(_rows);

		});
	});
});

function queryPlayerStats(callback) {

}

// start our server, listening on port 3000
var server=app.listen(3000,function(){
	console.log("We have started our server on port 3000");
});
