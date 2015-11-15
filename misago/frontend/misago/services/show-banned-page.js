(function (Misago) {
  'use strict';

  Misago.addService('show-banned-page', function(_) {
    _.showBannedPage = function(ban, changeState) {
      var component = _.component(
        'banned-page', _.models.deserialize('ban', ban));

      if (typeof changeState === 'undefined' || !changeState) {
        _.title.set(gettext("You are banned"));
        window.history.pushState({}, "", _.context.BANNED_URL);
      }

      _.mountPage(component);
    };
  });
}(Misago.prototype));
