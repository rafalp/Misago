(function (ns) {
  'use strict';

  ns.ForumLayout = {
    view: function(ctrl, _) {
      return m('.container', [
        m('h1', _.settings.forum_name),
        m('hr'),
        m('#route-outlet', 'Current route will be rendered here.'),
        m('hr'),
        m('p', 'Forum footer goes here.')
      ]);
    }
  };
}(Misago.prototype));
