(function (ns) {
  'use strict';

  ns.ForumNavbar = {
    view: function(ctrl, _) {
      var desktop_navbar = [];

      if (_.settings.forum_branding_display) {
        desktop_navbar.push(
          m('a.navbar-brand', {href: _.router.url('misago:index')}, [
            m('img', {
              src: _.router.staticUrl('misago/img/site-logo.png'),
              alt: _.settings.forum_name
            }),
            _.settings.forum_branding_text
          ])
        );
      }

      return m('nav.navbar.navbar-default.navbar-static-top[role="navigation"]', [
        m('.container.navbar-full.hidden-xs.hidden-sm', desktop_navbar)
      ]);
    }
  };
}(Misago.prototype));
