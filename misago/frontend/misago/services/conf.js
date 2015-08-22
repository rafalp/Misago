(function (_) {
  'use strict';

  _.Conf = function(_) {
    _.settings = _.get(_.preloaded_data, 'SETTINGS', {});
  };
}(Misago.prototype));
