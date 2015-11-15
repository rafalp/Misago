(function (Misago) {
  'use strict';

  var banExpirationMessage = {
    controller: function(ban, container) {
      var _ = container || ban;

      if (container) {
        return ban;
      } else {
        return _.models.deserialize('ban', _.context.ban);
      }
    },
    view: function(ban) {
      var expirationMessage = null;
      if (ban.expires_on) {
        if (ban.expires_on.isAfter(moment())) {
          expirationMessage = interpolate(
            gettext('This ban expires %(expires_on)s.'),
            {'expires_on': ban.expires_on.fromNow()},
            true);
        } else {
          expirationMessage = gettext('This ban has expired.');
        }
      } else {
        expirationMessage = gettext('This ban is permanent.');
      }

      return m('p', expirationMessage);
    }
  };

  Misago.addService('component:ban-expiration-message', function(_) {
    _.component('ban-expiration-message', banExpirationMessage);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
