/* global ace */
import Ember from 'ember';

export default Ember.Service.extend({
  includedJs: false,
  loadedJs: false,

  edit: function(elementId) {
    return ace.edit(elementId);
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
    this.loader.require('misago/js/ace.js');
    this.set('includedJs', true);
  },

  _loadingPromise: function() {
    var self = this;
    return new Ember.RSVP.Promise(function(resolve) {
      var wait = function() {
        if (typeof ace === "undefined") {
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
    // we have already loaded ace.js, resolve away!
    return new Ember.RSVP.Promise(function(resolve) {
      Ember.run(null, resolve);
    });
  }
});
