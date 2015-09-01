(function (ns) {
  'use strict';

  ns.Conf = function(_) {
    _.settings = ns.get(_.context, 'SETTINGS', {});
  };
}(Misago.prototype));
