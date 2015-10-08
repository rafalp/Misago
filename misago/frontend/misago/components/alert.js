(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var alert = {
    classes: {
      'info': 'alert-info',
      'success': 'alert-success',
      'warning': 'alert-warning',
      'error': 'alert-danger'
    },
    view: function(ctrl, _) {
      return m(
        '.alerts',
        {
          config: persistent,
          class: _.alert.isVisible ? 'in' : 'out'
        },
        m('p.alert',
          {
            class: this.classes[_.alert.type]
          },
          _.alert.message
        )
      );
    }
  };

  Misago.addService('component:alert', {
    factory: function(_) {
      _.component('alert', alert);
    },
    after: 'components'
  });
}(Misago.prototype));
