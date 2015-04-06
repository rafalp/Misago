/* global zxcvbn */
import Ember from 'ember';

export default Ember.Service.extend({
  includedJs: false,
  loadedJs: false,

  scorePassword: function(password, inputs) {
    // 0-4 score, the more the stronger password
    return zxcvbn(password, inputs).score;
  },

  loadLibrary: function() {
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
    Ember.$.getScript(this.get('_includedJsPath'));
    this.set('includedJs', true);
  },

  _includedJsPath: function() {
    return this.get('staticUrl') + 'misago/js/zxcvbn.js';
  }.property(),

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
          resolve();
        }
      };
      wait();
    });
  },

  _loadedPromise: function() {
    // we have already loaded zxcvbn.js, resolve away!
    return new Ember.RSVP.Promise(function(resolve) {
      resolve();
    });
  }
});
