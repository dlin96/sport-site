var yamlParser = require('js-yaml');
var fs = require('fs');

module.exports.loadConfig = function loadConfig(filepath) {
    try {
        var doc = yamlParser.safeLoad(fs.readFileSync(filepath));
        // const doc = {
        //     "user": process.env.DB_USER,
        //     "password": process.env.DB_PW,
        //     "host": process.env.DB_URL,
        //     "port": process.env.DB_PORT,
        //     "database": process.env.DB
        // };

        // console.log(process.env.DB_URL);
        return doc;
    } catch(e) {
        console.log(e);
    }
};
