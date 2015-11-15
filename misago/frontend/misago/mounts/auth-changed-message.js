(function (Misago) {
  'use strict';

  var mount = document.getElementById('auth-changed-message-mount');

  Misago.addService('mount:auth-changed-message', {
    factory: function(_) {
      m.mount(mount, _.component('auth-changed-message'));
    },
    destroy: function() {
      m.mount(mount, null);
    }
  },
  {
    before: 'mount:page-component'
  });
}(Misago.prototype));
