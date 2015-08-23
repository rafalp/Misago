(function (ns) {
  'use strict';

  ns.Conf = function(_) {
    _.settings = ns.get(_.preloaded_data, 'SETTINGS', {});
  };
}(Misago.prototype));
