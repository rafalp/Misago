(function (Misago) {
  'use strict';

  Misago.startsWith = function(string, beginning) {
    return string.indexOf(beginning) === 0;
  };

  Misago.endsWith = function(string, tail) {
    return string.indexOf(tail, string.length - tail.length) !== -1;
  };
}(Misago.prototype));
