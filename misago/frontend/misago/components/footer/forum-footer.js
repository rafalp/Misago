(function (Misago) {
  'use strict';

  Misago.ForumFooter = {
    view: function(ctrl, _) {
      var nav = null;
      if (Misago.FooterNav.isVisible(_.settings)) {
        nav = _.component(Misago.FooterNav);
      }

      return m('footer.forum-footer', [
        m('.container',
          m('.footer-content', [
            nav,
            _.component(Misago.FooterMisagoBranding)
          ])
        )
      ]);
    }
  };
}(Misago.prototype));
