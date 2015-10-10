(function (Misago) {
  'use strict';

  var header = {
    view: function(ctrl, options) {
      return m('.page-header',
        m('.container', [
          m('h1', options.title),
        ])
      );
    }
  };

  Misago.addService('component:header', function(_) {
    _.component('header', header);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
