(function (Misago) {
  'use strict';

  var nav = {
    controller: function(_) {
      return {
        showSignIn: function() {
          _.modal('sign-in');
        }
      };
    },
    view: function(ctrl, _) {
      return m('div.nav.nav-guest', [
        _.component('button', {
          class: '.navbar-btn.btn-default',
          onclick: ctrl.showSignIn,
          disabled: ctrl.isBusy,
          label: gettext('Sign in')
        }),
        _.component('navbar:register-button', '.navbar-btn.btn-primary')
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:guest-nav', function(_) {
    _.component('navbar:desktop:guest-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
