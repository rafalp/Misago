(function (Misago) {
  'use strict';

  var mount = document.getElementById('misago-page-mount');

  Misago.addService('show-banned-page', function(_) {
    _.showBannedPage = function(ban) {
      var component = _.component(
        'banned-page', _.models.deserialize('ban', ban));

      _.title.set(gettext('You are banned'));
      window.history.pushState({}, "", _.context.BANNED_URL);
      m.mount(mount, component);
    };
  });
}(Misago.prototype));
