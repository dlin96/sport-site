// var http = require('http');
var express = require('express');
// var bodyParser = require('body-parser');
var cors = require('cors');

var app = express();

app.use(cors());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.get('/', (req, res) => res.send('ss-server'));

// routes 
var playerCompRoutes = require('./routes/playercomp');
var depthChartRoutes = require('./routes/depthcharts');
app.use('/playercomp/', playerCompRoutes); 
app.use('/depthchart/', depthChartRoutes);

// start our server, listening on port 8000
let port = process.env.PORT;
if(port == null || port == "") port=8000;
app.listen(port, () => {
    console.log("We have started our server on port 8000");
});
