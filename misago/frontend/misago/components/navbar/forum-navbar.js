(function (ns) {
  'use strict';

  ns.ForumNavbar = {
    view: function(ctrl, _) {
      var desktop_navbar = [];

      if (_.settings.forum_branding_display) {
        desktop_navbar.push(_.component(ns.BrandFull, _.settings.forum_branding_text));
      }

      desktop_navbar.push(m('ul.nav.navbar-nav', [
        m('li', m("a", {config: m.route, href: _.router.url('index')}, 'Index')),
        m('li', m("a", {config: m.route, href: _.router.url('test')}, 'Test'))
      ]));

      return m('nav.navbar.navbar-default.navbar-static-top[role="navigation"]', [
        m('.container.navbar-full.hidden-xs.hidden-sm', desktop_navbar)
      ]);
    }
  };
}(Misago.prototype));
