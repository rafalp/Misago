(function (Misago) {
  'use strict';

  var navbar = {
    style: '.navbar.navbar-misago.navbar-default.navbar-static-top',
    mainNav: function(_) {
      var links = [
        {
          label: gettext("Threads"),
          icon: 'chat',
          url: _.router.url('index')
        },
        {
          label: gettext("Forums"),
          icon: 'forum',
          url: '/not-yet/forums/'
        },
        {
          label: gettext("Users"),
          icon: 'group',
          url: '/not-yet/users/'
        }
      ];

      return links;
    },
    view: function(ctrl, _) {
      var links = this.mainNav(_);

      return m('nav' + this.style + '[role="navigation"]', [
        _.component('navbar:desktop', links),
        _.component('navbar:mobile', links)
      ]);
    }
  };

  Misago.addService('component:navbar', function(_) {
    _.component('navbar', navbar);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
