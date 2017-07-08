var http = require('http');
var mysql = require('mysql');
var prompt = require('prompt');
var express = require('express');

var app = express();

// http.createServer(function(req, res) {
// 	console.log("listening on port 3000");
// 	var callback = function(err, result) {
// 		res.writeHead(200, {
// 			'Content-Type' : 'application/json'
// 		});
// 		console.log('json:', result);
// 		res.end(result);
// 	};

// 	queryDb(callback);

// }).listen(3000);

app.set('views',__dirname + '/public');
app.use(express.static(__dirname + '/js'));
app.set('view engine', 'ejs');
app.engine('html', require('ejs').renderFile);

app.get('/', function(req, res) {
	res.sendFile(__dirname + '/public/index.html');
});

app.get('/search', function(req, res) {
	// create mysql connection 
	var con = mysql.createConnection({
		host: "sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
		user: "root",
		password: "warriors73-9",
		database: "nbadb"
	});

	// connect to the db
	con.connect();

	query = 'SELECT fullName FROM players WHERE fullName LIKE "%' + req.query.key+'%"';
	con.query(query, function(err, rows, fields) {
		var data=[];
		for(var i=0; i<rows.length;i++) {
			data.push(rows[i].fullName);
		}

		// for(var i=0; i<data.length; i++) {
		// 	console.log(data[i]);
		// }
		console.log(rows.length);
		json = JSON.stringify(data);
		console.log(json);
		res.end(json);
	});
});

function queryDb(callback) {
	// create mysql connection 
	var con = mysql.createConnection({
		host: "sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
		user: "root",
		password: "warriors73-9",
		database: "nbadb"
	});

	// connect to the db
	con.connect(function(err) {
		if (err) throw err;
		console.log("Connected!");
	});

	prompt.start();
	prompt.get(['playerId_one', 'playerId_two'], function(err, result) {
		if(err) {console.log("Error");
			return;
		};

		var query = "SELECT * FROM stats WHERE playerId=? UNION ALL SELECT * FROM stats WHERE playerId=?"
		con.query(query, [result.playerId_one, result.playerId_two], function(err, result, fields) {
			if (err) throw err;
			console.log(result);

			json = JSON.stringify(result);

			con.end();
			console.log(json);
			callback(null, json);
		});
	});
}

var server=app.listen(3000,function(){
	console.log("We have started our server on port 3000");
});
