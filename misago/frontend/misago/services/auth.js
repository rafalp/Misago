(function (Misago) {
  'use strict';

  var Auth = function(_) {
    _.user = _.models.deserialize('user', _.context.user);

    // Access controls
    this.denyAuthenticated = function(message) {
      if (_.user.isAuthenticated) {
        throw new Misago.PermissionDenied(
          message || gettext("This page is not available to signed in users."));
      }
    };

    this.denyAnonymous = function(message) {
      if (_.user.isAnonymous) {
        throw new Misago.PermissionDenied(
          message || gettext("This page is not available to guests."));
      }
    };
  };

  Misago.addService('auth', function(_) {
    return new Auth(_);
  },
  {
    after: 'model:user'
  });
}(Misago.prototype));
