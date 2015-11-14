(function (Misago) {
  'use strict';

  var Dropdown = function(_) {
    var slots = {};

    this.toggle = function(elementId, component) {
      var element = document.getElementById(elementId);

      if (element.hasChildNodes() && slots[elementId] === component) {
        slots[elementId] = null;
        m.mount(element, null);
        $(element).removeClass('open');
      } else {
        console.log(element.hasChildNodes());
        slots[elementId] = component;
        m.mount(element, _.component(component));
        $(element).addClass('open');
      }
    };

    this.destroy = function() {
      var element = null;

      for (var elementId in slots) {
        if (slots.hasOwnProperty(elementId)) {
          element = document.getElementById(elementId);
          if (element && element.hasChildNodes()) {
            m.mount(element, null);
          }
        }
      }
    };
  };

  Misago.addService('dropdown', {
    factory: function(_) {
      return new Dropdown(_);
    },
    destroy: function(_) {
      _.dropdown.destroy();
    }
  },
  {
    before: 'components'
  });
}(Misago.prototype));
