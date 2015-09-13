(function (Misago) {
  'use strict';

  var RunLoop = function(_) {
    var self = this;

    this._intervals = {};

    this.run = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        var result = callable(_);
        if (result !== false) {
          self.run(callable, name, delay);
        }
      }, delay);
    };

    this.runOnce = function(callable, name, delay) {
      this._intervals[name] = window.setTimeout(function() {
        callable(_);
      }, delay);
    };

    this.stop = function() {
      for (var name in this._intervals) {
        if (this._intervals.hasOwnProperty(name)) {
          window.clearTimeout(this._intervals[name]);
          delete this._intervals[name];
        }
      }
    };
  };

  Misago.RunLoopFactory = {
    factory: function(_) {
      return new RunLoop(_);
    },

    destroy: function(_) {
      _.runloop.stop();
    }
  };
}(Misago.prototype));
