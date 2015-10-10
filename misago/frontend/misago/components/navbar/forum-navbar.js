(function (Misago) {
  'use strict';

  var navbar = {
    view: function(ctrl, _) {
      var style = '.navbar.navbar-default.navbar-static-top';
      return m('nav' + style + '[role="navigation"]', [
        _.component('navbar:desktop')
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
