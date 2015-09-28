(function (Misago) {
  'use strict';

  function persistent(el, isInit, context) {
    context.retain = true;
  }

  Misago.SignInModal = {
    view: function() {
      return m('.modal-dialog[role="document"]',
        {config: persistent},
        m('.modal-content', [
          m('.modal-header',
            m('h4#misago-modal-label.modal-title', 'Sign in modal!')
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
}(Misago.prototype));
