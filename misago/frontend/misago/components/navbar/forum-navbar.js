(function (Misago) {
  'use strict';

  Misago.ForumNavbar = {
    view: function(ctrl, _) {
      var style = '.navbar.navbar-default.navbar-static-top';
      return m('nav' + style + '[role="navigation"]', [
        _.component(Misago.DesktopForumNavbar)
      ]);
    }
  };
}(Misago.prototype));
