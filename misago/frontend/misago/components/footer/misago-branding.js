(function (ns) {
  'use strict';

  ns.FooterMisagoBranding = {
    view: function() {
      return m('a.misago-branding[href=http://misago-project.org]', [
        "powered by ", m('strong', "misago")
      ]);
    }
  };
}(Misago.prototype));
