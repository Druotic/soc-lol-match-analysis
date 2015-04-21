var api = require('leagueapi');
var config = require('./config');

api.init(config.apiKey, config.region);
