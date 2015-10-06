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
      if (name && component) {
        component.container = _;
        this._routes[name] = m.component(boilerplate(component), _);
      } else {
        return this._routes[name];
      }
    };
  });
}(Misago.prototype));
