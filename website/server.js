var http = require('http');
var express = require('express');
var bodyParser = require('body-parser');
var iniParser = require('ini');
var MongoClient = require('mongodb').MongoClient
var cors = require('cors');

var app = express();
app.use(cors());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});
/*
 * Should return the index page. Root route.
 * NOTE: as of right now, index needs to be renamed. 
 * For temporary needs, the filename will vary.
 */
// app.get('/', function(req, res) {
// 	res.sendFile(app.get('views') + '/depthchart.html');
// });

/*
 * function name: querydb
 * purpose: query the depth-chart db for the specifc teamname. 
 * parameters: teamname - teamname to query
 *             callback - callback function to handle result. 
 * return: none
 */ 

 var dbEndpoint = 'mongodb://localhost:27017'; 
 var ffdb = "fantasy-football-db";

let querydb = (teamname, callback) => {
    MongoClient.connect(dbEndpoint, (err, client) => {
	    if (err) throw err;

        // TODO: error condition to check if teamname is in db 
        // handle error condition where teamname is empty
        var db = client.db(ffdb);
        
        try {
            db.collection(teamname).find().toArray( function(err, result) {     
                if (err) throw err;       
                callback(result);
            });
        }	

        catch(e) {
            console.log(e);
        }
    });
}

/*
 * METHOD: GET
 * Route: /depth-chart/
 * Param(s): teamname - team name to look up in db
 */
app.get('/depthchart/', (req, res) => {
    console.log("GET /depthchart/");
    console.log("teamname: " + req.query.teamname);   

    var teamname = req.query.teamname.toLowerCase();

    // TODO: client-side input sanitization
    querydb(teamname, function(result) {
        return res.json(result); 
    });
}); 

app.get('/teams/', (req, res) => {
    console.log("getting teamnames");

    MongoClient.connect(dbEndpoint, (err, client) => {
        if (err) throw err;

        var db = client.db(ffdb);
        db.listCollections().toArray(function(err, colInfo) {
            if (err) throw err; 
            var teamnames = [];

            colInfo.map( entry => {
                teamnames.push(entry["name"]);
            })
            return res.json(teamnames);
        });
    });
})

// start our server, listening on port 8000
var server=app.listen(8000, () => {
	console.log("We have started our server on port 8000");
});
