(function (Misago) {
  'use strict';

  var boilerplate = function(component) {
    // Component already boilerplated (this may happen in tests)
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
      if (this.isActive && error.status) {
        if (this.vm && this.vm.onerror) {
          this.vm.onerror(error, this.container);
        } else {
          this.container.router.errorPage(error);
        }
      } else {
        throw error;
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
      } else if (component) {
        component.container = _;
        this._routes[name] = boilerplate(component);
      } else {
        throw '"' + name + '" route is not registered and can\'t be created';
      }
    };
  });
}(Misago.prototype));
