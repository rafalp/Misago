(function (Misago) {
  'use strict';

  var header = {
    view: function(ctrl, title) {
      return m('.modal-header', [
        m('button.close[type="button"]',
          {'data-dismiss': 'modal', 'aria-label': gettext('Close')},
          m('span', {'aria-hidden': 'true'}, m.trust('&times;'))
        ),
        m('h4#misago-modal-label.modal-title', title)
      ]);
    }
  };

  Misago.addService('component:modal:header', function(_) {
    _.component('modal:header', header);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
