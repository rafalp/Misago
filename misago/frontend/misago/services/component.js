(function (ns) {
  'use strict';

  ns.ComponentFactory = function(_) {
    // Component factory
    _.component = function() {
      var arguments_array = [];
      for (var i = 0; i < arguments.length; i += 1) {
        arguments_array.push(arguments[i]);
      }

      arguments_array.push(_);
      return m.component.apply(undefined, arguments_array);
    };
  };
}(Misago.prototype));
