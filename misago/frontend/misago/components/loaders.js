(function (ns) {
  'use strict';

  ns.Loader = {
    view: function() {
      return m('.loader.sk-folding-cube', [
        m('.sk-cube1.sk-cube'),
        m('.sk-cube2.sk-cube'),
        m('.sk-cube4.sk-cube'),
        m('.sk-cube3.sk-cube')
      ]);
    }
  };

  ns.LoadingPage = {
    view: function(ctrl, _) {
      return m('.page.page-loading',
        _.component(ns.Loader)
      );
    }
  };
} (Misago.prototype));
