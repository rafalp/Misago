(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var forumLayout = {
    view: function(ctrl, _) {
      return [
        _.component('auth-changed-message'),
        _.component('alert'),
        _.component('navbar'),
        m('#router-fixture', {config: persistent}),
        _.component('footer'),
        _.component('modal')
      ];
    }
  };

  Misago.addService('component:layout', function(_) {
    _.component('forum-layout', forumLayout);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
