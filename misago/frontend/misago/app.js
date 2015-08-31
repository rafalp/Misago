/* global -Misago */
/* exported Misago */
(function () {
  'use strict';

  window.Misago = function() {

    var ns = Object.getPrototypeOf(this);
    var self = this;

    // Preloaded data
    this.preloaded_data = {
      // Empty settings
      SETTINGS: {}
    };

    // Services
    this._services = [];
    this.addService = function(name, factory, order) {
      this._services.push({
        name: name,
        item: factory,
        after: this.get(order, 'after'),
        before: this.get(order, 'before')
      });
    };

    this._initServices = function(services) {
      var ordered_services = new ns.OrderedList(services).order(false);
      ordered_services.forEach(function (item) {
        var factory = null;
        if (item.item.factory !== undefined) {
          factory = item.item.factory;
        } else {
          factory = item.item;
        }

        var service_instance = factory(self);
        if (service_instance) {
          self[item.name] = service_instance;
        }
      });
    };

    this._destroyServices = function(services) {
      var ordered_services = new ns.OrderedList(services).order();
      ordered_services.reverse();
      ordered_services.forEach(function (item) {
        if (item.destroy !== undefined) {
          item.destroy(self);
        }
      });
    };

    this.registerCoreServices = function() {
      this.addService('conf', ns.Conf);
      this.addService('component', ns.ComponentFactory);
      this.addService('router', ns.RouterFactory);
      this.addService('api', ns.Api);
      this.addService('outlet', ns.Outlet);
      this.addService('title', ns.PageTitle);
      this.addService('start-routing', ns.startRouting);
    };

    // App init/destory
    this.setup = false;
    this.init = function(setup) {
      this.setup = {
        fixture: ns.get(setup, 'fixture', null),
        in_test: ns.get(setup, 'in_test', false)
      };

      this._initServices(this._services);
    };

    this.destroy = function() {
      this._destroyServices();
    };
  };
}());
