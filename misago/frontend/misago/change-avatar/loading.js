(function (Misago) {
  'use strict';

  var component = {
    view: function(ctrl, vm, _) {
      return m('.modal-body.modal-loading',
        _.component('loader')
      );
    }
  };

  Misago.addService('component:change-avatar:loading', function(_) {
    _.component('change-avatar:loading', component);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
