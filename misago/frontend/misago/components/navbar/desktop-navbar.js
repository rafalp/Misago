(function (Misago) {
  'use strict';

  Misago.DesktopForumNavbar = {
    view: function(ctrl, _) {
      var menu = [];

      if (_.settings.forum_branding_display) {
        menu.push(
          _.component(Misago.BrandFull, _.settings.forum_branding_text));
      }

      menu.push(m('ul.nav.navbar-nav', [
        m('li',
          m("a", {config: m.route, href: _.router.url('index')}, 'Index')
        )
      ]));

      menu.push(_.component(Misago.NavbarGuestMenu));

      return m('.container.navbar-full.hidden-xs.hidden-sm', menu);
    }
  };
}(Misago.prototype));
