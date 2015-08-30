(function (ns) {
  'use strict';

  ns.startsWith = function(string, beginning) {
    return string.indexOf(beginning) === 0;
  };

  ns.endsWith = function(string, tail) {
    return string.indexOf(tail, string.length - tail.length) !== -1;
  };
}(Misago.prototype));
