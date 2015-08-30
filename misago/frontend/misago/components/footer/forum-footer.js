(function (ns) {
  'use strict';

  ns.ForumFooter = {
    view: function(ctrl, _) {
      var nav = null;
      if (ns.FooterNav.isVisible(_.settings)) {
        nav = _.component(ns.FooterNav);
      }

      return m('footer.forum-footer', [
        m('.container',
          m('.footer-content', [
            nav,
            _.component(ns.FooterMisagoBranding)
          ])
        )
      ]);
    }
  };
}(Misago.prototype));
