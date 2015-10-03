(function (Misago) {
  'use strict';

  var noop = function() {};

  Misago.route = function(component) {
    /*
      Boilerplate for Misago top-level components
    */

    // Component state
    component.isActive = true;

    // Wrap controller to store lifecycle methods
    var __controller = component.controller || noop;
    component.controller = function() {
      component.isActive = true;

      var controller = __controller.apply(component, arguments) || {};

      // wrap onunload for lifestate
      var __onunload = controller.onunload || noop;
      controller.onunload = function() {
        __onunload.apply(component, arguments);
        component.isActive = false;
      };

      return controller;
    };

    // Add state callbacks to View-Model
    if (component.vm && component.vm.init) {
      // wrap vm.init in promise handler
      var __init = component.vm.init;
      component.vm.init = function() {
        var initArgs = arguments;
        var promise = __init.apply(component.vm, initArgs);

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

      var __view = component.view;
      component.view = function() {
        if (component.vm.isReady) {
          return __view.apply(component, arguments);
        } else {
          return component.loading.apply(component, arguments);
        }
      };
    }

    return component;
  };
}(Misago.prototype));
