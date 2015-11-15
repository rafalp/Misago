(function (Misago) {
  'use strict';

  var bannedPage = {
    view: function(ctrl, ban, _) {
      var error_message = [];

      if (ban.message.html) {
        error_message.push(m('.lead', m.trust(ban.message.html)));
      } else {
        error_message.push(m('p.lead', ban.message.plain));
      }

      error_message.push(_.component('ban-expiration-message', ban));

      return m('.page.page-error.page-error-banned',
        m('.container',
          m('.message-panel', [
            m('.message-icon',
              m('span.material-icon', 'highlight_off')
            ),
            m('.message-body', error_message)
          ])
        )
      );
    }
  };

  Misago.addService('component:banned-page', function(_) {
    _.component('banned-page', bannedPage);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
