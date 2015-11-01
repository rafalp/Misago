(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var authChanged = {
    refresh: function() {
      window.location.reload();
    },
    view: function(ctrl, _) {
      var message = '';

      var options = {
        config: persistent,
        class: (_.auth.isDesynced ? 'show' : null)
      };

      if (_.auth.isDesynced) {
        if (_.auth.newUser && _.auth.newUser.isAuthenticated) {
          message = gettext("You have signed in as %(username)s. Please refresh this page before continuing.");
          message = interpolate(message, {username: _.auth.newUser.username}, true);
        } else {
          message = gettext("%(username)s, you have been signed out. Please refresh this page before continuing.");
          message = interpolate(message, {username: _.user.username}, true);
        }
      }

      return m('.auth-changed-message', options,
        m('',
          m('.container', [
            m('p',
              message
            ),
            m('p', [
              m('button.btn.btn-default[type="button"]', {onclick: this.refresh},
                gettext("Reload page")
              ),
              m('span.hidden-xs.hidden-sm.text-muted',
                gettext("or press F5 key.")
              )
            ])
          ])
        )
      );
    }
  };

  Misago.addService('component:auth-changed-message', function(_) {
    _.component('auth-changed-message', authChanged);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
