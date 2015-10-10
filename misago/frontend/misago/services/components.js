(function (Misago) {
  'use strict';

  var component = function(name, component) {
    if (this._components[name]) {
      if (arguments.length > 1) {
        var argumentsArray = [this._components[name]];
        for (var i = 1; i < arguments.length; i += 1) {
          argumentsArray.push(arguments[i]);
        }
        argumentsArray.push(this);
        return m.component.apply(undefined, argumentsArray);
      } else {
        return m.component(this._components[name], this);
      }
    } else {
      this._components[name] = component;
    }
  };

  Misago.addService('components', function(_) {
    _._components = {};
    _.component = component;
  });
}(Misago.prototype));
