(function (Misago) {
  'use strict';

  var forum = {
    view: function(ctrl, _) {
      return m('', [
        _.component('header', {
          title: gettext("Options")
        }),
        m('.container',
          m('p', 'Lorem ipsum dolor met.')
        )
      ]);
    }
  };

  Misago.addService('component:options:nav:dropdown', function(_) {
    _.component('options:nav:dropdown', forum);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
