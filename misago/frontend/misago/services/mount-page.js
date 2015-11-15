(function (Misago) {
  'use strict';

  var mount = document.getElementById('page-mount');

  Misago.addService('mount-page', function(_) {
    _.mountPage = function(component) {
      m.mount(mount, component);
    };
  });
}(Misago.prototype));
