(function (Misago) {
  'use strict';

  var menu = {
    controller: function() {
      return {
        logout: function() {
          $('#hidden-logout-form').submit();
        }
      };
    },
    view: function(ctrl, _) {
      return m('div.nav.nav-user', [
        m('p.navbar-text',
          _.user.username
        ),
        m('button.navbar-btn.btn.btn-default.navbar-right',
          {
            onclick: ctrl.logout.bind(ctrl)
          },
          gettext("Logout")
        )
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:user-menu', function(_) {
    _.component('navbar:desktop:user-menu', menu);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
