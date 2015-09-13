(function (Misago) {
  'use strict';

  Misago.has = function(obj, key) {
    if (obj) {
      return obj.hasOwnProperty(key);
    } else {
      return false;
    }
  };

  Misago.get = function(obj, key, value) {
    if (Misago.has(obj, key)) {
      return obj[key];
    } else if (value !== undefined) {
      return value;
    } else {
      return undefined;
    }
  };

  Misago.pop = function(obj, key, value) {
    var returnValue = Misago.get(obj, key, value);
    if (Misago.has(obj, key)) {
      delete obj[key];
    }
    return returnValue;
  };
}(Misago.prototype));
