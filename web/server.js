var http = require('http');
var express = require('express');
var bodyParser = require('body-parser');
var iniParser = require('ini');
var MongoClient = require('mongodb').MongoClient
var cors = require('cors');

var app = express();

app.set('views', __dirname + '/src');
app.use(express.static(__dirname + '/public'));
app.use(cors());

/*
 * Should return the index page. Root route.
 * NOTE: as of right now, index needs to be renamed. 
 * For temporary needs, the filename will vary.
 */
app.get('/', function(req, res) {
	res.sendFile(app.get('views') + '/depthchart.html');
});


/*
 * function name: querydb
 * purpose: query the depth-chart db for the specifc teamname. 
 * parameters: teamname - teamname to query
 *             callback - callback function to handle result. 
 * return: none
 */ 
let querydb = (teamname, callback) => {
    MongoClient.connect('mongodb://localhost:27017', (err, client) => {
	    if (err) throw err;

        // TODO: error condition to check if teamname is in db 
	    var db = client.db("fantasy-football-db");	
	    db.collection(teamname).find().toArray( function(err, result) {
		    if (err) throw err;
		
            callback(result);
		    client.close()
	    });

    });
}


/*
 * METHOD: GET
 * Route: /depth-chart/
 * Param(s): teamname - team name to look up in db
 */
app.get('/depth-chart/', (req, res) => {
    console.log("GET /depth-chart/");
    console.log("teamname: " + req.query.teamname);   

    // TODO: client-side input sanitization
    querydb(req.query.teamname, function(result) {
        console.log(result);
        res.json(result); 
    });
}); 

// start our server, listening on port 8000
var server=app.listen(8000, () => {
	console.log("We have started our server on port 8000");
});
