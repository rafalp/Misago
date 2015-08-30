(function (ns) {
  'use strict';

  ns.Outlet = {
    factory: function(_) {
      if (_.setup.fixture) {
        m.mount(document.getElementById(_.setup.fixture),
                _.component(ns.ForumLayout));
      }
    },

    destroy: function(_) {
      if (_.setup.fixture) {
        m.mount(_.setup.fixture, null);
      }
    }
  };
}(Misago.prototype));
