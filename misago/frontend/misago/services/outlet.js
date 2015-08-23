(function (ns) {
  'use strict';

  ns.Outlet = {
    factory: function(_) {
      if (_._outlet) {
        m.mount(document.getElementById(_._outlet),
                _.component(ns.ForumLayout));
      }
    },

    destroy: function(_) {
      if (_._outlet) {
        m.mount(_._outlet, null);
      }
    }
  };
}(Misago.prototype));
