(function (Misago) {
  'use strict';

  var persistent = function(el, isInit, context) {
    context.retain = true;
  };

  var markup = {
    view: function(ctrl, content) {
      return m('article.misago-markup', {config: persistent},
        m.trust(content)
      );
    }
  };

  Misago.addService('component:markup', {
    factory: function(_) {
      _.component('markup', markup);
    },
    after: 'components'
  });
}(Misago.prototype));
