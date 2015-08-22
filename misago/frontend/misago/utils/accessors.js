(function (ns) {
  'use strict';

  ns.has = function(obj, key) {
    if (obj !== undefined) {
      return obj.hasOwnProperty(key);
    } else {
      return false;
    }
  };

  ns.get = function(obj, key, value) {
    if (ns.has(obj, key)) {
      return obj[key];
    } else if (value !== undefined) {
      return value;
    } else {
      return undefined;
    }
  };

  ns.pop = function(obj, key, value) {
    var returnValue = ns.get(obj, key, value);
    if (ns.has(obj, key)) {
      delete obj[key];
    }
    return returnValue;
  };
}(Misago.prototype));
