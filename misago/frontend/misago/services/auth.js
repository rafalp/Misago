(function (Misago) {
  'use strict';

  var Auth = function(_) {
    _.user = _.models.deserialize('user', _.context.user);
  };

  Misago.addService('auth', function(_) {
    return new Auth(_);
  },
  {
    after: 'model:user'
  });
}(Misago.prototype));
