(function (Misago) {
  'use strict';

  var dropdown = {
    controller: function(_) {
      return {
        showSignIn: function() {
          _.modal('sign-in');
        }
      };
    },
    view: function(ctrl, _) {
      return m('ul.dropdown-menu.user-dropdown.dropdown-menu-right[role="menu"]',
        m('li.guest-preview', [
          m('h4',
            gettext("You are browsing as guest.")
          ),
          m('p',
            gettext('Sign in or register to start and participate in discussions.')
          ),
          m('.row', [
            m('.col-xs-6',
              _.component('button', {
                class: '.btn.btn-default.btn-block',
                onclick: ctrl.showSignIn,
                disabled: ctrl.isBusy,
                label: gettext('Sign in')
              })
            ),
            m('.col-xs-6',
              _.component(
                'navbar:register-button', '.btn.btn-primary.btn-block')
            )
          ])
        ])
      );
    }
  };

  Misago.addService('component:navbar:dropdown:guest', function(_) {
    _.component('navbar:dropdown:guest', dropdown);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
