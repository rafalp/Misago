(function (Misago) {
  'use strict';

  Misago.addService('mount-page', function(_) {
    _.mountPage = function(component) {
      var mount = document.getElementById('page-mount');
      m.mount(mount, component);
    };
  });
}(Misago.prototype));
