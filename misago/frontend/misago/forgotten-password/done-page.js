(function (Misago) {
  'use strict';

  var donePage = {
    controller: function(user, _) {
      _.title.set(gettext("Your password has been changed."));

      return {
        showSignIn: function() {
          _.modal('sign-in');
        }
      };
    },
    view: function(ctrl, user) {
      var button = 'button.btn.btn-primary[type="button"]';
      var message = gettext("%(username)s, your password has been changed successfully.");

      return m('.page.page-message.page-message-success.page-forgotten-password-done',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'check')
            ),
            m('.message-body', [
              m('p.lead',
                interpolate(message, {
                  username: user.username
                }, true)
              ),
              m('p',
                gettext("You will have to sign in using new password before continuing.")
              ),
              m('p',
                m(button, {onclick: ctrl.showSignIn},
                  gettext("Sign in")
                )
              )
            ])
          ])
        )
      );
    }
  };

  Misago.addService('component:forgotten-password:done-page', function(_) {
    _.component('forgotten-password:done-page', donePage);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
