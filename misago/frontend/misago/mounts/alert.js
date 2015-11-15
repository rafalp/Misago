(function (Misago) {
  'use strict';

  var mount = document.getElementById('alert-mount');

  Misago.addService('mount:alert', {
    factory: function(_) {
      m.mount(mount, _.component('alert'));
    },
    destroy: function() {
      m.mount(mount, null);
    }
  },
  {
    before: 'mount:page-component'
  });
}(Misago.prototype));
