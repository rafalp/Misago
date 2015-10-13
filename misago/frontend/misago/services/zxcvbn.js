/* global zxcvbn */
(function (Misago) {
  'use strict';

  var Zxcvbn = function(_) {
    this.included = false;

    this.scorePassword = function(password, inputs) {
      // 0-4 score, the more the stronger password
      return zxcvbn(password, inputs).score;
    };

    // loading
    this.include = function() {
      _.include('misago/js/zxcvbn.js');
      this.included = true;
    };

    var wait = function(promise) {
      if (typeof zxcvbn !== "undefined") {
        promise.resolve();
      } else {
        _.runloop.runOnce(function() {
          wait(promise);
        }, 'loading-zxcvbn', 150);
      }
    };

    var deferred = m.deferred();
    this.load = function() {
      if (!this.included) {
        this.include();
      }
      wait(deferred);
      return deferred.promise;
    };
  };

  Misago.addService('zxcvbn', function(_) {
    return new Zxcvbn(_);
  },
  {
    after: 'include'
  });
}(Misago.prototype));
