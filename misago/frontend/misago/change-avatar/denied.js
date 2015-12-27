(function (Misago) {
  'use strict';

  var component = {
    view: function(ctrl, rejection) {
      var reason = null;

      if (rejection.reason) {
        reason = m.trust(rejection.reason);
      }

      return m('.modal-body.modal-message', [
        m('.message-icon',
          m('span.material-icon', 'check')
        ),
        m('.message-body', [
          m('p.lead',
            rejection.detail
          ),
          reason
        ])
      ]);
    }
  };

  Misago.addService('component:change-avatar:denied', function(_) {
    _.component('change-avatar:denied', component);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
