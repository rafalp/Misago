(function (Misago) {
  'use strict';

  var bannedPage = {
    view: function(ctrl, ban) {
      var error_message = [];

      if (ban.message.html) {
        error_message.push(m('.lead', m.trust(ban.message.html)));
      } else {
        error_message.push(m('p.lead', gettext('You are banned.')));
      }

      var expirationMessage = null;
      if (ban.expires_on) {
        if (ban.expires_on.isAfter(moment())) {
          expirationMessage = interpolate(
            gettext('This ban expires %(expires_on)s.'),
            {'expires_on': ban.expires_on.fromNow()},
            true);
        } else {
          expirationMessage = gettext('This ban has expired.');
        }
      } else {
        expirationMessage = gettext('This ban is permanent.');
      }
      error_message.push(m('p', expirationMessage));

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
