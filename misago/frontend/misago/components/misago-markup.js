(function (ns) {
  'use strict';

  var setupMarkup = function(el, isInit, context) {
    context.retain = true;
  };

  ns.MisagoMarkup = {
    view: function(ctrl, content) {
      return m('article.misago-markup', {config: setupMarkup}, m.trust(content));
    }
  };
}(Misago.prototype));
