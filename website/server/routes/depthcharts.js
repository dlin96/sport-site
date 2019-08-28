var express = require('express');
var router = express.Router();

var dc_controller = require('../controllers/DepthChartController');

/*
 * METHOD: GET
 * Route: /depthchart/
 * Param(s): None
 */

 router.get('/', (req, res) => {
     res.render("pages/depthchart.ejs");
 })

/*
 * METHOD: GET
 * Route: /depthchart/team
 * Param(s): teamname - team name to look up in db
 */
router.get('/team/', dc_controller.getDepthChart); 

module.exports = router;