(function (Misago) {
  'use strict';

  var nav = {
    view: function(ctrl, links) {
      return m('ul.nav.navbar-nav', [
        links.map(function(link) {
          return m('li',
            m("a", link.config || {href: link.url},
              link.label
            )
          );
        })
      ]);
    }
  };

  Misago.addService('component:navbar:desktop:main-nav', function(_) {
    _.component('navbar:desktop:main-nav', nav);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
