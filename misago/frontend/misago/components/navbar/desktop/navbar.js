(function (Misago) {
  'use strict';

  var navbar = {
    view: function(ctrl, _) {
      var menu = [];

      if (_.settings.forum_branding_display) {
        menu.push(
          _.component('navbar:desktop:brand', _.settings.forum_branding_text));
      }

      menu.push(m('ul.nav.navbar-nav', [
        m('li',
          m("a", {config: m.route, href: _.router.url('index')}, 'Index')
        )
      ]));

      menu.push(_.component('navbar:desktop:guest-menu'));

      return m('.container.navbar-full.hidden-xs.hidden-sm', menu);
    }
  };

  Misago.addService('component:navbar:desktop', function(_) {
    _.component('navbar:desktop', navbar);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
