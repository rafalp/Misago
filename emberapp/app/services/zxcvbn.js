/* global zxcvbn */
import Ember from 'ember';

export default Ember.Service.extend({
  includedJs: false,
  loadedJs: false,

  scorePassword: function(password, inputs) {
    // 0-4 score, the more the stronger password
    return zxcvbn(password, inputs).score;
  },

  load: function() {
    if (!this.get('includedJs')) {
      this._includeJs();
    }

    if (!this.get('loadedJs')) {
      return this._loadingPromise();
    } else {
      return this._loadedPromise();
    }
  },

  _includeJs: function() {
    this.loader.require('misago/js/zxcvbn.js');
    this.set('includedJs', true);
  },

  _loadingPromise: function() {
    var self = this;
    return new Ember.RSVP.Promise(function(resolve) {
      var wait = function() {
        if (typeof zxcvbn === "undefined") {
          Ember.run.later(function () {
            wait();
          }, 200);
        } else {
          self.set('loadedJs', true);
          Ember.run(null, resolve);
        }
      };
      wait();
    });
  },

  _loadedPromise: function() {
    // we have already loaded zxcvbn.js, resolve away!
    return new Ember.RSVP.Promise(function(resolve) {
      Ember.run(null, resolve);
    });
  }
});
