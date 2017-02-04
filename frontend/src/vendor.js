var jQuery = require('jquery'); // jshint ignore:line
var moment = require('moment');

global.$ = jQuery;
global.jQuery = jQuery;
global.moment = moment;

require('bootstrap-transition');
require('bootstrap-affix');
require('bootstrap-modal');
require('bootstrap-dropdown');

require('cropit');
require('waypoints');

require('highlight');