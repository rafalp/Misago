(function (Misago) {
  'use strict';

  var dropdown = {
    class: '.dropdown-menu.user-dropdown.dropdown-menu-right',

    controller: function() {
      return {
        logout: function() {
          var decision = confirm(gettext("Are you sure you want to sign out?"));
          if (decision) {
            $('#hidden-logout-form').submit();
          }
        }
      };
    },
    view: function(ctrl, _) {
      return m('ul' + this.class + '[role="menu"]', [
        m('li.dropdown-header',
          m('strong',
            _.user.username
          )
        ),
        m('li.divider'),
        m('li',
          m('a', {href: '/not-yet/'}, [
            m('span.material-icon',
              'account_circle'
            ),
            gettext("See your profile")
          ])
        ),
        m('li',
          m('a', {href: '/not-yet/'}, [
            m('span.material-icon',
              'done_all'
            ),
            gettext("Edit account")
          ])
        ),
        m('li',
          m('button.btn-link[type="button"]', [
            m('span.material-icon',
              'face'
            ),
            gettext("Change avatar")
          ])
        ),
        m('li.divider'),
        m('li.dropdown-footer',
          m('button.btn.btn-default.btn-block', {onclick: ctrl.logout},
            gettext("Logout")
          )
        )
      ]);
    }
  };

  Misago.addService('component:navbar:dropdown:user', function(_) {
    _.component('navbar:dropdown:user', dropdown);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
