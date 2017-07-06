var mysql = require('mysql');
var prompt = require('prompt');

// create mysql connection
var con = mysql.createConnection({
	host: "sports-db.ceutzulos0qe.us-west-1.rds.amazonaws.com",
	user: "root",
	password: "warriors73-9"
});

// connect to the db
con.connect(function(err) {
	if (err) throw err;
	console.log("Connected!");
});

con.query("use nbadb", function(err, result) {
	if (err) throw err;
	console.log("use db");
});

con.query("describe players", function(err, result, fields) {
	if (err) throw err;
	console.log(result);
});

