(function (Misago) {
  'use strict';

  var RunLoop = function(_) {
    var self = this;

    this._intervals = {};

    var stopInterval = function(name) {
      if (self._intervals[name]) {
        window.clearTimeout(self._intervals[name]);
        self._intervals[name] = null;
      }
    };

    this.run = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        stopInterval(name);
        var result = callable(_);
        if (result !== false) {
          self.run(callable, name, delay);
        }
      }, delay);
    };

    this.runOnce = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        stopInterval(name);
        callable(_);
      }, delay);
    };

    this.stop = function(name) {
      for (var loop in this._intervals) {
        if (!name || name === loop) {
          stopInterval(loop);
        }
      }
    };
  };

  Misago.addService('runloop', {
    factory: function(_) {
      return new RunLoop(_);
    },

    destroy: function(_) {
      _.runloop.stop();
    }
  });
}(Misago.prototype));
