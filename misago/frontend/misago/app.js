/* global -Misago */
/* exported Misago */
(function () {
  'use strict';

  window.Misago = function() {

    var ns = Object.getPrototypeOf(this);
    var self = this;

    // Context data
    this.context = {
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
      var orderedServices = new ns.OrderedList(services).order(false);
      orderedServices.forEach(function (item) {
        var factory = null;
        if (item.item.factory !== undefined) {
          factory = item.item.factory;
        } else {
          factory = item.item;
        }

        var serviceInstance = factory(self);
        if (serviceInstance) {
          self[item.name] = serviceInstance;
        }
      });
    };

    this._destroyServices = function(services) {
      var orderedServices = new ns.OrderedList(services).order();
      orderedServices.reverse();
      orderedServices.forEach(function (item) {
        if (item.destroy !== undefined) {
          item.destroy(self);
        }
      });
    };

    this.registerCoreServices = function() {
      this.addService('conf', ns.Conf);
      this.addService('component', ns.ComponentFactory);
      this.addService('router', ns.RouterFactory);
      this.addService('ajax', ns.ajax);
      this.addService('api', ns.api);
      this.addService('outlet', ns.Outlet);
      this.addService('title', ns.PageTitle);
      this.addService('start-routing', ns.startRouting);
    };

    // App init/destory
    this.setup = false;
    this.init = function(setup) {
      this.setup = {
        fixture: ns.get(setup, 'fixture', null),
        inTest: ns.get(setup, 'inTest', false)
      };

      this._initServices(this._services);
    };

    this.destroy = function() {
      this._destroyServices();
    };
  };
}());
