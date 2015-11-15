(function (Misago) {
  'use strict';

  var nav = {
    controller: function(_) {
      return {
        openUserMenu: function() {
          _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:user');
          return false;
        }
      };
    },
    view: function(ctrl, _) {
      var config = {
        onclick: ctrl.openUserMenu,
        href: _.user.absolute_url
      };

      return m('a', config,
        _.component('user-avatar', _.user, 64)
      );
    }
  };

  Misago.addService('component:navbar:compact:user-nav', function(_) {
    _.component('navbar:compact:user-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
