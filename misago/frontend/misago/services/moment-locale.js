(function (Misago) {
  'use strict';

  Misago.setMomentLocale = function() {
    moment.locale($('html').attr('lang'));
  };
}(Misago.prototype));
