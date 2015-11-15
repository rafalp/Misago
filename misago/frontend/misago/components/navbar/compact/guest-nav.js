(function (Misago) {
  'use strict';

  var nav = {
    controller: function(_) {
      return {
        openUserMenu: function() {
          _.dropdown.toggle('navbar-dropdown', 'navbar:dropdown:guest');
        }
      };
    },
    view: function(ctrl, _) {
      return m('button', {type: 'button', onclick: ctrl.openUserMenu},
        _.component('user-avatar', null, 64)
      );
    }
  };

  Misago.addService('component:navbar:compact:guest-nav', function(_) {
    _.component('navbar:compact:guest-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
