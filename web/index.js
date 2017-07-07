var http = require('http');
var mysql = require('mysql');
var express = require('express');

var app = express();

http.createServer(function(req, res) {
	console.log("listening on port 3000");
	var callback = function(err, result) {
		res.writeHead(200, {
			'Content-Type' : 'application/json'
		});
		console.log('json:', result);
		res.end(result);
	};

	queryDb(callback);

}).listen(3000);

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

	con.query("SELECT * FROM players WHERE lastName='curry'", function(err, result, fields) {
		if (err) throw err;
		console.log(result);

		json = JSON.stringify(result);

		con.end();
		console.log('json-result: ', json);
		callback(null, json);
	});
}