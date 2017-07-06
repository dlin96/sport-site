var http = require('http');
var express = require('express');

var app = express();

http.createServer(function(req, res) {
	var callback = function(err, result) {
		res.writeHead(200, {
			'Content-Type' : 'application/json'
		});
		console.log('json:', result);
		res.json(result);
	};


}).listen(3000);