(function (Misago) {
  'use strict';

  var dropdown = {
    class: '.dropdown-menu.user-dropdown.dropdown-menu-right',

    controller: function(_) {
      return {
        openAvatarOptions: function() {
          _.modal('change-avatar', _.user);
        },
        logout: function() {
          var decision = confirm(gettext("Are you sure you want to sign out?"));
          if (decision) {
            $('#hidden-logout-form').submit();
          }
        }
      };
    },
    view: function(ctrl, _) {
      var changeAvatarConfig = {onclick: ctrl.openAvatarOptions};
      var logoutConfig = {onclick: ctrl.logout};

      return m('ul' + this.class + '[role="menu"]', [
        m('li.dropdown-header',
          m('strong',
            _.user.username
          )
        ),
        m('li.divider'),
        m('li',
          m('a', {href: _.user.absolute_url}, [
            m('span.material-icon',
              'account_circle'
            ),
            gettext("See your profile")
          ])
        ),
        m('li',
          m('a', {href: _.context.USERCP_URL}, [
            m('span.material-icon',
              'done_all'
            ),
            gettext("Change options")
          ])
        ),
        m('li',
          m('button.btn-link[type="button"]', changeAvatarConfig, [
            m('span.material-icon',
              'face'
            ),
            gettext("Change avatar")
          ])
        ),
        m('li.divider'),
        m('li.dropdown-footer',
          m('button.btn.btn-default.btn-block', logoutConfig,
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
