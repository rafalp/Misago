(function (Misago) {
  'use strict';

  Misago.addService('conf', function(_) {
    _.settings = Misago.get(_.context, 'SETTINGS', {});
  });
}(Misago.prototype));
