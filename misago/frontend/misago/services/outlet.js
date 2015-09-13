(function (Misago) {
  'use strict';

  Misago.OutletFactory = {
    factory: function(_) {
      if (_.setup.fixture) {
        m.mount(document.getElementById(_.setup.fixture),
                _.component(Misago.ForumLayout));
      }
    },

    destroy: function(_) {
      if (_.setup.fixture) {
        m.mount(_.setup.fixture, null);
      }
    }
  };
}(Misago.prototype));
