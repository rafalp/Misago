(function (Misago) {
  'use strict';

  var forum = {
    view: function(ctrl, _) {
      return m('.list-group.nav-side', [

      ]);
    }
  };

  Misago.addService('component:options:nav:side', function(_) {
    _.component('options:nav:side', forum);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
