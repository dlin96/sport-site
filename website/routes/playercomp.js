var express = require('express');
var router = express.Router();

// import controllers here
var pc_controller = require('../controllers/PlayerCompController');

/*
 * METHOD: GET
 * Route: /playercomp/
 * Param(s): teamname - team name to look up in db
 */
router.get('/', pc_controller.playerStatGet);

module.exports = router;