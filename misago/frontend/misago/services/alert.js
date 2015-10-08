(function (Misago) {
  'use strict';

  var ALERT_BASE_DISPLAY_TIME = 5 * 1000;
  var ALERT_LENGTH_FACTOR = 70;
  var ALERT_MAX_DISPLAY_TIME = 9 * 1000;
  var ALERT_HIDE_ANIMATION_LENGTH = 300;

  var Alert = function(_) {
    var self = this;

    this.id = 0;
    this.type = 'info';
    this.message = null;
    this.isVisible = false;

    var show = function(type, message) {
      m.startComputation();

      self.id += 1;
      self.type = type;
      self.message = message;
      self.isVisible = true;

      m.endComputation();

      var displayTime = ALERT_BASE_DISPLAY_TIME;
      displayTime += message.length * ALERT_LENGTH_FACTOR;
      if (displayTime > ALERT_MAX_DISPLAY_TIME) {
        displayTime = ALERT_MAX_DISPLAY_TIME;
      }

      var id  = self.id;
      _.runloop.runOnce(function () {
        if (self.id === id) {
          m.startComputation();
          self.isVisible = false;
          m.endComputation();
        }
      }, 'flash-message-hide', displayTime);
    };

    var set = function(type, message) {
      if (self.isVisible) {
        self.isVisible = false;
        _.runloop.runOnce(function () {
          show(type, message);
        }, 'flash-message-show', ALERT_HIDE_ANIMATION_LENGTH);
      } else {
        show(type, message);
      }
    };

    this.info = function(message) {
      set('info', message);
    };

    this.success = function(message) {
      set('success', message);
    };

    this.warning = function(message) {
      set('warning', message);
    };

    this.error = function(message) {
      set('error', message);
    };
  };

  Misago.addService('alert', {
    factory: function(_) {
      return new Alert(_);
    }
  });
}(Misago.prototype));
