(function (Misago) {
  'use strict';

  var mount = document.getElementById('page-component');

  Misago.addService('mount:page-component', {
    factory: function(_) {
      if (mount) {
        m.mount(mount, _.component(mount.dataset.componentName));
      }
    },
    destroy: function() {
      if (mount) {
        m.mount(mount, null);
      }
    }
  },
  {
    before: '_end'
  });
}(Misago.prototype));
