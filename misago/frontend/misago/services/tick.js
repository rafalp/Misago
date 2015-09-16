(function (Misago) {
  'use strict';

  Misago.addService('start-tick', function(_) {
    var ticks = m.prop();

    _.runloop.run(function() {
      m.startComputation();
      // just tick once a minute so stuff gets rerendered
      ticks(ticks() + 1);
      // syncing dynamic timestamps, etc ect
      m.endComputation();
    }, 'tick', 60000);
  });
}(Misago.prototype));
