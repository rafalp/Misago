(function (Misago) {
  'use strict';

  var mountDesktop = document.getElementById('misago-user-menu-mount');
  var mountCompact = document.getElementById('misago-user-menu-compact-mount');

  Misago.addService('mount:user-menu', {
    factory: function(_) {
      if (_.user.isAuthenticated) {
        m.mount(mountDesktop, _.component('navbar:desktop:user-nav'));
        m.mount(mountCompact, _.component('navbar:compact:user-nav'));
      } else {
        m.mount(mountDesktop, _.component('navbar:desktop:guest-nav'));
        m.mount(mountCompact, _.component('navbar:compact:guest-nav'));
      }
    },
    destroy: function() {
      m.mount(mountDesktop, null);
      m.mount(mountCompact, null);
    }
  },
  {
    before: 'mount:page-component'
  });
}(Misago.prototype));
