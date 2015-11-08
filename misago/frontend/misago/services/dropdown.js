(function (Misago) {
  'use strict';

  var dropdownConfig = function(element, isInit, context) {
    if (!isInit) {
      context.retain = true;

      $(element).on('click', function() {
        $(element).removeClass('open');
      });

      context.onunload = function() {
        $(element).removeClass('open');
        $(element).off();
      };
    }
  };

  var Dropdown = function(_) {
    var slots = {};

    this.slot = function(name) {
      return m('#dropdown-' + name + '.dropdown.mobile-dropdown', {
        config: dropdownConfig
      });
    };

    this.toggle = function(slot, component) {
      var element = document.getElementById('dropdown-' + slot);

      if (element.hasChildNodes() && slots[slot] === component) {
        slots[slot] = null;
        m.mount(element, null);
        $(element).removeClass('open');
      } else {
        slots[slot] = component;
        m.mount(element, _.component(component));
        $(element).addClass('open');
      }
    };
  };

  Misago.addService('dropdown', {
    factory: function(_) {
      return new Dropdown(_);
    }
  },
  {
    before: 'components'
  });
}(Misago.prototype));
