(function (Misago) {
  'use strict';

  var noop = function() {};

  Misago.stateHooks = function(component, loadingState, errorState) {
    /*
      Boilerplate for Misago components with lifecycles
    */

    // Component boilerplated (this may happen in tests)
    if (component._hasLifecycleHooks) {
      return component;
    }
    component._hasLifecycleHooks = true;

    // Component active state
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
      // setup default loading view
      if (!component.loading) {
        var loadingHandler = loadingState.bind(component);
        component.loading = loadingHandler;
      }

      var _view = component.view;
      component.view = function() {
        if (component.vm.isReady) {
          return _view.apply(component, arguments);
        } else {
          return component.loading.apply(component, arguments);
        }
      };

      var errorHandler = errorState.bind(component);

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
              errorHandler(error);
            }
          });
        }
      };
    }

    return component;
  };
}(Misago.prototype));
