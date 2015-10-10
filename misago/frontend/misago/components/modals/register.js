(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  var register = {
    view: function() {
      return m('.modal-dialog.modal-lg[role="document"]',
        {config: persistent},
        m('.modal-content', [
          m('.modal-header',
            m('h4#misago-modal-label.modal-title', 'Register in modal!')
          ),
          m('.modal-body', [
            m('p', 'Lorem ipsum dolor met sit amet elit.'),
            m('p', [
              'Si vis pacem ',
              m('a', {href: '/'}, 'bellum'),
              ' sequitat.'
            ])
          ])
        ])
      );
    }
  };

  Misago.addService('modal:register', function(_) {
    _.modal('register', register);
  },
  {
    after: 'modals'
  });
}(Misago.prototype));
