(function (ns) {
  'use strict';

  ns.ForumLayout = {
    view: function(ctrl, _) {
      return [
        _.component(ns.ForumNavbar)
      ];
    }
  };
}(Misago.prototype));
