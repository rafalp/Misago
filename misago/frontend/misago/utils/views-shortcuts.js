(function (ns) {
  'use strict';

  ns.loadingPage = function(_) {
    return m('.page.page-loading', _.component(ns.Loader));
  };
} (Misago.prototype));
