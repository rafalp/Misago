(function (Misago) {
  'use strict';

  var menu = {
    controller: function(_) {
      return {
        showSignIn: function() {
          _.modal('sign-in');
        },

        isBusy: false,
        showRegister: function() {
          if (_.settings.account_activation === 'closed') {
            _.alert.info(gettext("New registrations are currently disabled."));
          } else {
            m.startComputation();
            this.isBusy = true;
            m.endComputation();

            var self = this;
            m.sync([
              _.zxcvbn.load(),
              _.captcha.load()
            ]).then(function() {
              _.modal('register');
            }, function() {
              _.alert.error(gettext('Registation is not available now due to an error.'));
            }).then(function() {
              m.startComputation();
              self.isBusy = false;
              m.endComputation();
            });
          }
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
        _.component('button', {
          class: '.navbar-btn.btn-primary',
          onclick: ctrl.showRegister.bind(ctrl),
          loading: ctrl.isBusy,
          label: gettext('Register')
        })
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
