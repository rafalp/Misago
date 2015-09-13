(function (Misago) {
  'use strict';

  Misago.addService('forum-layout', {
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
  }, {before: 'start-routing'});
}(Misago.prototype));
