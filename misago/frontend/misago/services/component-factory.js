(function (Misago) {
  'use strict';

  Misago.addService('components-factory', function(_) {
    // Component factory
    _.component = function() {
      var argumentsArray = [];
      for (var i = 0; i < arguments.length; i += 1) {
        argumentsArray.push(arguments[i]);
      }

      argumentsArray.push(_);
      return m.component.apply(undefined, argumentsArray);
    };
  });
}(Misago.prototype));
