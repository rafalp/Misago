(function (Misago) {
  'use strict';

  var menu = {
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

  Misago.addService('component:navbar:desktop:guest-menu', {
    factory: function(_) {
      _.component('navbar:desktop:guest-menu', menu);
    },
    after: 'components'
  });
}(Misago.prototype));
