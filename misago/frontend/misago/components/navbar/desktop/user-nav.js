(function (Misago) {
  'use strict';

  var nav = {
    controller: function() {
      return {
        dropdownToggle: {
          href: '/not-yet/',

          'data-toggle': 'dropdown',
          'data-misago-routed': 'false',

          'aria-haspopup': 'true',
          'aria-expanded': 'false'
        }
      };
    },
    view: function(ctrl, _) {
      return m('ul.nav.navbar-nav.nav-user', [
        m('li.dropdown', [
          m('a.dropdown-toggle[role="button"]', ctrl.dropdownToggle,
            _.component('user-avatar', _.user, 64)
          ),
          _.component('navbar:dropdown:user')
        ])
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:user-nav', function(_) {
    _.component('navbar:desktop:user-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
