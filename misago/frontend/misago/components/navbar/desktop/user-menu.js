(function (Misago) {
  'use strict';

  var menu = {
    controller: function() {
      return {
        isBusy: m.prop(false),
        logout: function() {
          if (!this.isBusy()) {
            this.isBusy(true);
            $('#hidden-logout-form').submit();
          }
        }
      };
    },
    view: function(ctrl, _) {
      return m('div.nav.user-nav', [
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
