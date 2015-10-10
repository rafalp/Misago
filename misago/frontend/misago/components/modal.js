(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var modal = {
    view: function() {
      return m(
        '#misago-modal.modal.fade[role="dialog"]',
        {
          config: persistent,
          tabindex: "-1",
          "aria-labelledby": "misago-modal-label"
        }
      );
    }
  };

  Misago.addService('component:modal', function(_) {
    _.component('modal', modal);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
