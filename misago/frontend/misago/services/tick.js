(function (Misago) {
  'use strict';

  Misago.startTick = function(_) {
    _.runloop.run(function() {
      m.startComputation();
      // just tick once a minute so stuff gets rerendered
      // syncing dynamic timestamps, etc ect
      m.endComputation();
    }, 'tick', 60000);
  };
}(Misago.prototype));
