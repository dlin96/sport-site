var express = require('express');
var router = express.Router();

// import controllers here
var pc_controller = require('../controllers/PlayerCompController');

/*
 * METHOD: GET
 * Route: /playercomp/
 * Param(s): None
 */
router.get('/', pc_controller.playerStatGet);

/*
 * METHOD: POST
 * Route: /playercomp/search
 * Param(s): playername - name of player user is searching for
 */
router.post('/search', pc_controller.autocompleteSearch);

module.exports = router;