(function (Misago) {
  'use strict';

  var brand = {
    view: function(ctrl, branding, _) {
      var children = [
        m('img', {
          src: _.router.staticUrl('misago/img/site-logo.png'),
          alt: _.settings.forum_name
        })
      ];

      if (branding) {
        children.push(branding);
      }

      return m('a.navbar-brand', {href: _.router.url('index')}, children);
    }
  };

  Misago.addService('component:navbar:desktop:brand', function(_) {
    _.component('navbar:desktop:brand', brand);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
