var admin = require('./adminFuncs');
var MongoClient = require('mongodb').MongoClient
    , Db = require('mongodb').Db
    , Server = require('mongodb').Server;

/*
 * function name: querydb
 * purpose: query the depth-chart db for the specifc teamname. 
 * parameters: teamname - teamname to query
 *             callback - callback function to handle result. 
 * return: none
 */ 

var ffdb = "depth-chart";

let querydb = (teamname, callback) => {
    connectMongoDB(function(client, err) {
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
    console.log(__dirname);
    dbConfig = admin.loadConfig(__dirname + "/mongoconf.yaml");
    username = dbConfig["username"];
    password = dbConfig["passwd"];
    ipAddr = dbConfig["ip_addr"];
    port = dbConfig["port"];

    var dbEndpoint = 'mongodb://nfldb:ramona3374@localhost:27017/?authMechanism=DEFAULT&authSource=depth-chart'; 

    MongoClient.connect(dbEndpoint, {useNewUrlParser: true, useUnifiedTopology: true}, (err, client) => {
        if(err) throw err;
        callback(client);
    });
}

let capitalize = teamname => {
    teamname = teamname.toLowerCase();
    return teamname[0].toUpperCase() + teamname.slice(1);
}

exports.getDepthChart = (req, res) => {
    console.log("GET /depthchart/");
    console.log("teamname: " + req.query.teamname);   

    var teamname = req.query.teamname.toLowerCase();

    // TODO: client-side input sanitization
    querydb(teamname, function(result) {
        result[0]["team_name"] = capitalize(result[0]["team_name"]);
        res.render("pages/depthchart.ejs", {"result": result[0]}); 
    })
};