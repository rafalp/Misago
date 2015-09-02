(function (Misago) {
  'use strict';

  Misago.FooterMisagoBranding = {
    view: function() {
      return m('a.misago-branding[href=http://misago-project.org]', [
        "powered by ", m('strong', "misago")
      ]);
    }
  };
}(Misago.prototype));
