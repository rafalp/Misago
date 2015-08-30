(function (ns) {
  'use strict';

  ns.PageHeader = {
    view: function(ctrl, options) {
      return m('.page-header',
        m('.container', [
          m('h1', options.title),
        ])
      );
    }
  };
}(Misago.prototype));
