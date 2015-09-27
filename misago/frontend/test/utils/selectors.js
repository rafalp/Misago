(function () {
  'use strict';

  window.getElement = function(selector) {
    return $('#misago-fixture ' + selector);
  };

  window.getElementText = function(selector) {
    return $.trim(getElement(selector).text());
  };
}());
