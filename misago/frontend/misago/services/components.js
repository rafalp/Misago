(function (Misago) {
  'use strict';

  var component = function(name, component) {
    if (this._components[name]) {
      var argumentsArray = [this._components[name]];
      for (var i = 1; i < arguments.length; i += 1) {
        argumentsArray.push(arguments[i]);
      }
      argumentsArray.push(this);
      return m.component.apply(undefined, argumentsArray);
    } else {
      this._components[name] = component;
    }
  };

  Misago.addService('components', function(_) {
    _._components = {};
    _.component = component;
  });
}(Misago.prototype));
