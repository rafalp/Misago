(function (Misago) {
  'use strict';

  Misago.Conf = function(_) {
    _.settings = Misago.get(_.context, 'SETTINGS', {});
  };
}(Misago.prototype));
