import Ember from 'ember';

export default Ember.Service.extend({
  includedJs: false,
  loadedJs: false,

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
    Ember.$.getScript(this.get('_includedJsPath'));
    this.set('includedJs', true);
  },

  _includedJsPath: function() {
    return this.get('staticUrl') + 'misago/js/cropit.js';
  }.property(),

  _loadingPromise: function() {
    var self = this;
    return new Ember.RSVP.Promise(function(resolve) {
      var wait = function() {
        if (typeof Ember.$.fn.cropit === "undefined") {
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
    // we have already loaded croppic.js, resolve away!
    return new Ember.RSVP.Promise(function(resolve) {
      Ember.run(null, resolve);
    });
  }
});
