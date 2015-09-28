(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  Misago.ForumModal = {
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
}(Misago.prototype));
