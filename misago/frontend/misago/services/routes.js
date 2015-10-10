(function (Misago) {
  'use strict';

  var boilerplate = function(component) {
    /*
      Boilerplate for Misago top-level components
    */

    // Component boilerplated (this may happen in tests)
    if (component._hasRouteBoilerplate) {
      return component;
    }
    component._hasRouteBoilerplate = true;

    // Add lifecycle hooks
    var loadingView = function () {
      var _ = this.container;
      return m('.page.page-loading',
        _.component('loader')
      );
    };

    var errorHandler = function(error) {
      if (this.isActive) {
        this.container.router.errorPage(error);
      }
    };

    return Misago.stateHooks(component, loadingView, errorHandler);
  };

  Misago.addService('routes', function(_) {
    _._routes = {};
    _.route = function(name, component) {
      if (this._routes[name]) {
        if (arguments.length > 1) {
          var argumentsArray = [this._routes[name]];
          for (var i = 1; i < arguments.length; i += 1) {
            argumentsArray.push(arguments[i]);
          }
          argumentsArray.push(this);
          return m.component.apply(undefined, argumentsArray);
        } else {
          return m.component(this._routes[name], this);
        }
      } else {
        component.container = _;
        this._routes[name] = boilerplate(component);
      }
    };
  });
}(Misago.prototype));
