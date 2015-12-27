var jQuery = require('jQuery'); // jshint ignore:line

global.$ = jQuery;
global.jQuery = jQuery;

require('bootstrap-transition');
require('bootstrap-affix');
require('bootstrap-modal');
require('bootstrap-dropdown');

require('jquery-mockjax')(jQuery, window);
$.mockjaxSettings.logging = false;

require("babel-polyfill");
