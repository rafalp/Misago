// Mithril.js window mock factory
// jshint ignore: start
(function (global) {
  'use strict';

  window.mock = function() {
    var window = {}
    window.document = global.document;
    window.scrollTo = function() {};
    window.cancelAnimationFrame = global.cancelAnimationFrame;
    window.requestAnimationFrame = global.requestAnimationFrame;
    window.XMLHttpRequest = global.XMLHttpRequest;
    window.location = {search: "", pathname: "", hash: ""};
    window.history = {};
    window.history.$$length = 0;
    window.history.pushState = function(data, title, url) {
      window.history.$$length++
      window.location.pathname = window.location.search = window.location.hash = url
    };
    window.history.replaceState = function(data, title, url) {
      window.location.pathname = window.location.search = window.location.hash = url
    };
    return window;
  };
}(window));
