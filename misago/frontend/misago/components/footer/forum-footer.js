(function (Misago) {
  'use strict';

  var isMenuVisible = function(settings) {
    return [
      !!settings.forum_footnote,
      !!settings.terms_of_service,
      !!settings.terms_of_service_link,
      !!settings.privacy_policy,
      !!settings.privacy_policy_link
    ].indexOf(true) !== -1;
  };

  var footer = {
    view: function(ctrl, _) {
      var nav = null;
      if (isMenuVisible(_.settings)) {
        nav = _.component('footer:menu');
      }

      return m('footer.forum-footer', [
        m('.container',
          m('.footer-content', [
            nav,
            _.component('footer:branding')
          ])
        )
      ]);
    }
  };

  Misago.addService('component:footer', {
    factory: function(_) {
      _.component('footer', footer);
    },
    after: 'components'
  });
}(Misago.prototype));
