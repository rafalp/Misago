/* globals -Misago */
/* exported Misago */

var Misago = {

  // Namespaces
  component: {},
  template: {},

  // Initialization
  init: function() {
    var testservice = function(name) {
      return {
        init: function() {
          console.log('init:' + name);
        }
      };
    };

    this.addService('apple', testservice('apple'));
    this.addService('banana', testservice('banana'));
    this.addService('orange', testservice('orange'));
    this.addService('kiwi', testservice('kiwi'), {before: 'banana'});
    this.addService('melon', testservice('melon'), {after: 'potato'});
    this.addService('potato', testservice('potato'));

    this.initServices(this.services);
    this.renderLayout(document.getElementById('main'));
  },

  renderLayout: function(element) {
    return element;
  },

  // Services
  services: [],

  addService: function(name, service, order) {
    this.services.push({
      name: name,
      item: service,
      after: this.get(order, 'after'),
      before: this.get(order, 'before')
    });
  },

  initServices: function(services) {
    var ordered_services = this.OrderedList(services).order();
    ordered_services.forEach(function (item) {
      item.service.init();
    });
  },

  // Accessors utils
  has: function(obj, prop) {
    if (obj !== undefined) {
      return obj.hasOwnProperty(prop);
    } else {
      return false;
    }
  },

  get: function(obj, prop, value) {
    if (this.has(obj, prop)) {
      return obj[prop];
    } else if (value !== undefined) {
      return value;
    } else {
      return undefined;
    }
  }
};
