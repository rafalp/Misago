(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  Misago.ForumLayout = {
    view: function(ctrl, _) {
      return [
        _.component(Misago.ForumNavbar),
        m('#router-fixture', {config: persistent}),
        _.component(Misago.ForumFooter),
        m.component(Misago.ForumModal)
      ];
    }
  };
}(Misago.prototype));
