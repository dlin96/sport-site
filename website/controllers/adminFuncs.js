var yamlParser = require('js-yaml');
var fs = require('fs');

module.exports.loadConfig = function loadConfig(filepath) {
    try {
        var doc = yamlParser.safeLoad(fs.readFileSync(filepath));
        return doc;
    } catch(e) {
        console.log(e);
    }
};