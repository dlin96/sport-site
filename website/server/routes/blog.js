var express = require('express');
var router = express.Router();

// var blog = require('../controllers/BlogController.js');

router.get('/', (req, res) => {
    res.send("hello world");
});

module.exports = router;  
