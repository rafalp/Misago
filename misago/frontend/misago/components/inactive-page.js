(function (Misago) {
  'use strict';

  var inactivePage = {
    view: function(ctrl, activation, _) {
      var activateButton = null;

      if (activation.type === 'inactive_user') {
        activateButton = m('p',
          m('a', {href: _.context.REQUEST_ACTIVATION_URL},
            gettext("Activate your account.")
          )
        );
      }

      return m('.page.page-message.page-message-info',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'info_outline')
            ),
            m('.message-body', [
              m('p.lead',
                gettext("Your account is inactive.")
              ),
              m('p',
                activation.message
              ),
              activateButton
            ])
          ])
        )
      );
    }
  };

  Misago.addService('component:inactive-page', function(_) {
    _.component('inactive-page', inactivePage);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
