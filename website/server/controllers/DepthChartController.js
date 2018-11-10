var admin = require('./adminFuncs');
var MongoClient = require('mongodb').MongoClient;

/*
 * function name: querydb
 * purpose: query the depth-chart db for the specifc teamname. 
 * parameters: teamname - teamname to query
 *             callback - callback function to handle result. 
 * return: none
 */ 

var ffdb = "fantasy-football-db";

let querydb = (teamname, callback) => {
    connectMongoDB(function(client) {
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

// start server only on successful db connection
function connectMongoDB(callback) {
    dbConfig = admin.loadConfig("../fantasy-football/mongoconf.yaml");
    username = dbConfig["username"];
    password = dbConfig["passwd"];
    ipAddr = dbConfig["ip_addr"];
    port = dbConfig["port"];
    var dbEndpoint = 'mongodb://'+username+':'+password+'@'+ipAddr+':'+port; 

    MongoClient.connect(dbEndpoint, (err, client) => {
        if(err) throw err;
        callback(client);
    });
}

exports.getDepthChart = (req, res) => {
    console.log("GET /depthchart/");
    console.log("teamname: " + req.query.teamname);   

    var teamname = req.query.teamname.toLowerCase();

    // TODO: client-side input sanitization
    querydb(teamname, function(result) {
        return res.json(result); 
    })
};