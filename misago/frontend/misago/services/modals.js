(function (Misago) {
  'use strict';

  var boilerplate = function(component) {
    return component;
  };

  var modal = function(name, component) {
    if (this._modals[name]) {
      var argumentsArray = [this._modals[name]];
      for (var i = 1; i < arguments.length; i += 1) {
        argumentsArray.push(arguments[i]);
      }
      argumentsArray.push(this);
      this._modal.show(m.component.apply(m, argumentsArray));
    } else if (name) {
      this._modals[name] = boilerplate(component);
    } else {
      this._modal.hide();
    }
  };

  Misago.addService('modals', {
    factory: function(_) {
      _._modals = {};
      _.modal = modal;
    },
    after: '_modal'
  });
}(Misago.prototype));
