(function () {
  'use strict';

  window.getMisagoService = function(name) {
    var services = window.Misago.prototype._services;
    for (var i in services) {
      if (services[i].key === name) {
        return services[i].item;
      }
    }
    return null;
  };
}());
