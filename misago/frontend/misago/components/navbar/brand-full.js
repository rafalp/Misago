(function (Misago) {
  'use strict';

  Misago.BrandFull = {
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
}(Misago.prototype));
