var express = require('express');
var cors = require('cors');

var app = express();

// app.use(cors());
app.use(express.static(__dirname + "/public"));
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST');
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});
app.set('view engine', 'ejs');

app.get('/', (req, res) => res.render('pages/index'));

// routes 
let playerCompRoutes = require('./routes/playercomp');
let depthChartRoutes = require('./routes/depthcharts');
let blogRoute = require('./routes/blog');
app.use('/playercomp/', playerCompRoutes); 
app.use('/depthchart/', depthChartRoutes);
app.use('/blog/', blogRoute);

// start our server, listening on port 8000
let port = process.env.PORT;
if(port == null || port == "") port=8000;
app.listen(port, () => {
    console.log("We have started our server on port 8000");
});
