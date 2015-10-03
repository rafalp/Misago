(function (Misago) {
  'use strict';

  var loader = {
    view: function() {
      return m('.loader.sk-folding-cube', [
        m('.sk-cube1.sk-cube'),
        m('.sk-cube2.sk-cube'),
        m('.sk-cube4.sk-cube'),
        m('.sk-cube3.sk-cube')
      ]);
    }
  };

  Misago.addService('component:loader', {
    factory: function(_) {
      _.component('loader', loader);
    },
    after: 'components'
  });
} (Misago.prototype));
