(function (Misago) {
  'use strict';

  Misago.NavbarGuestMenu = {
    view: function(ctrl, _) {
      return m('div.nav.guest-nav', [
        m('button.navbar-btn.btn.btn-default',
          {onclick: function() {_.modal.show(Misago.SignInModal); }},
          gettext("Sign in")),
        m('button.navbar-btn.btn.btn-primary',
          {onclick: function() {_.modal.show(Misago.RegisterModal); }},
          gettext("Register"))
      ]);
    }
  };
}(Misago.prototype));
