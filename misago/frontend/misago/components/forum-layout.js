(function (ns) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  ns.ForumLayout = {
    view: function(ctrl, _) {
      return [
        _.component(ns.ForumNavbar),
        m('#router-fixture', {config: persistent}),
        _.component(ns.ForumFooter)
      ];
    }
  };
}(Misago.prototype));
