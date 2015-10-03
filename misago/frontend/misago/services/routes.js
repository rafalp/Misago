(function (Misago) {
  'use strict';

  var noop = function() {};

  var boilerplate = function(component) {
    /*
      Boilerplate for Misago top-level components
    */

    // Component state
    component.isActive = true;

    // Wrap controller to store lifecycle methods
    var _controller = component.controller || noop;
    component.controller = function() {
      component.isActive = true;

      var controller = _controller.apply(component, arguments) || {};

      // wrap onunload for lifestate
      var _onunload = controller.onunload || noop;
      controller.onunload = function() {
        _onunload.apply(component, arguments);
        component.isActive = false;
      };

      return controller;
    };

    // Add state callbacks to View-Model
    if (component.vm && component.vm.init) {
      // wrap vm.init in promise handler
      var _init = component.vm.init;
      component.vm.init = function() {
        var initArgs = arguments;
        var promise = _init.apply(component.vm, initArgs);

        if (promise) {
          promise.then(function() {
            if (component.isActive && component.vm.ondata) {
              var finalArgs = [];
              for (var i = 0; i < arguments.length; i++) {
                finalArgs.push(arguments[i]);
              }
              for (var f = 0; f < initArgs.length; f++) {
                finalArgs.push(initArgs[f]);
              }

              component.vm.ondata.apply(component.vm, finalArgs);
            }
          }, function(error) {
            if (component.isActive) {
              component.container.router.errorPage(error);
            }
          });
        }
      };

      // setup default loading view
      if (!component.loading) {
        component.loading = function () {
          var _ = this.container;
          return m('.page.page-loading',
            _.component('loader')
          );
        };
      }

      var _view = component.view;
      component.view = function() {
        if (component.vm.isReady) {
          return _view.apply(component, arguments);
        } else {
          return component.loading.apply(component, arguments);
        }
      };
    }

    return component;
  };

  Misago.addService('routes', function(_) {
    _._routes = {};
    _.route = function(name, component) {
      if (name && component) {
        component.container = _;
        this._routes[name] = boilerplate(component);
      } else {
        return this._routes[name];
      }
    };
  });
}(Misago.prototype));
