(function (Misago) {
  'use strict';

  var navbar = {
    view: function(ctrl, mainNav, _) {
      var brand = null;
      var user = null;

      if (_.settings.forum_branding_display) {
        brand = _.component(
          'navbar:desktop:brand', _.settings.forum_branding_text);
      }

      if (_.user.isAuthenticated) {
        user = _.component('navbar:desktop:user-nav');
      } else {
        user = _.component('navbar:desktop:guest-nav');
      }

      return m('.container.navbar-full.hidden-xs.hidden-sm', [
        brand,
        _.component('navbar:desktop:main-nav', mainNav),
        user
      ]);
    }
  };

  Misago.addService('component:navbar:desktop', function(_) {
    _.component('navbar:desktop', navbar);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
