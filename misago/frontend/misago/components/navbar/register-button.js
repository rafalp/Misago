(function (Misago) {
  'use strict';

  var button = {
    controller: function(style, _) {
      return {
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
    view: function(ctrl, style, _) {
      return _.component('button', {
        class: style,
        onclick: ctrl.showRegister.bind(ctrl),
        loading: ctrl.isBusy,
        label: gettext('Register')
      });
    }
  };

  Misago.addService('component:navbar:register-button', function(_) {
    _.component('navbar:register-button', button);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
