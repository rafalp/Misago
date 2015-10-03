(function (Misago) {
  'use strict';

  var branding = {
    view: function() {
      return m('a.misago-branding[href=http://misago-project.org]', [
        "powered by ", m('strong', "misago")
      ]);
    }
  };

  Misago.addService('component:footer:branding', {
    factory: function(_) {
      _.component('footer:branding', branding);
    },
    after: 'components'
  });
}(Misago.prototype));
