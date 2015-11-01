(function (Misago) {
  'use strict';

  var Auth = function(_) {
    var self = this;

    _.user = _.models.deserialize('user', _.context.user);

    // Auth state synchronization across tabs
    this.isDesynced = false; // becomes true if auth state between tabs differs
    this.newUser = null; // becomes user obj to which we want to sync

    var handleAuthChange = function(isAuthenticated) {
      if (!self.isDesynced) {
        m.startComputation();

        // display annoying "you were desynced" message
        self.isDesynced = true;

        if (isAuthenticated) {
          self.newUser = _.localstore.get('auth-user');
        }

        m.endComputation();
      }
    };

    var handleUserChange = function(newUser) {
      if (!self.isDesynced) {
        m.startComputation();

        if (_.user.id !== newUser.id) {
          self.isDesynced = true;
          self.newUser = newUser;
        } else if (newUser) {
          _.user = $.extend(_.user, newUser);
        }

        m.endComputation();
      }
    };

    var syncSession = function() {
      _.localstore.set('auth-user', _.user);
      _.localstore.set('auth-is-authenticated', _.user.isAuthenticated);

      _.localstore.watch('auth-is-authenticated', handleAuthChange);
      _.localstore.watch('auth-user', handleUserChange);
    };

    syncSession();

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

  Misago.addService('auth',
  function(_) {
    return new Auth(_);
  },
  {
    after: 'model:user'
  });
}(Misago.prototype));
