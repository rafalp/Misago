(function (Misago) {
  'use strict';

  var menu = {
    controller: function(_) {
      return {
        showSignIn: function() {
          _.modal('sign-in');
        },
        showRegister: function() {
          _.modal('register');
        }
      };
    },
    view: function(ctrl) {
      return m('div.nav.nav-guest', [
        m('button.navbar-btn.btn.btn-default',
          {
            onclick: ctrl.showSignIn
          },
          gettext("Sign in")
        ),
        m('button.navbar-btn.btn.btn-primary',
          {
            onclick: ctrl.showRegister
          },
          gettext("Register")
        )
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:guest-menu', function(_) {
    _.component('navbar:desktop:guest-menu', menu);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
