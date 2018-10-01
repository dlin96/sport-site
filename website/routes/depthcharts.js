var express = require('express');
var router = express.Router();

var dc_controller = require('../controllers/DepthChartController');

/*
 * METHOD: GET
 * Route: /depth-chart/
 * Param(s): teamname - team name to look up in db
 */
router.get('/', dc_controller.getDepthChart); 

module.exports = router;