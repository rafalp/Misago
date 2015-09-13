(function (Misago) {
  'use strict';

  Misago.addService('set-momentjs-locale', function() {
    moment.locale($('html').attr('lang'));
  });
}(Misago.prototype));
