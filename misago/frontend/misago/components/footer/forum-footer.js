(function (Misago) {
  'use strict';

  var footer = {
    hasNav: function(_) {
      return [
        !!_.settings.forum_footnote,
        !!_.settings.terms_of_service,
        !!_.settings.terms_of_service_link,
        !!_.settings.privacy_policy,
        !!_.settings.privacy_policy_link
      ].indexOf(true) !== -1;
    },
    view: function(ctrl, _) {
      var nav = null;
      if (this.hasNav(_)) {
        nav = _.component('footer:nav');
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

  Misago.addService('component:footer', function(_) {
    _.component('footer', footer);
  },
  {
    after: 'components'
  });
}(Misago.prototype));
