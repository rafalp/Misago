/* global grecaptcha */
import Ember from 'ember';
import NoCaptcha from 'misago/services/nocaptcha';

export default NoCaptcha.extend({
  baseUrl: 'https://www.google.com/recaptcha/api.js?render=explicit',
  field: 'recaptcha-field',
  includedJs: false,
  loadedJs: false,

  load: function() {
    // Load reCaptcha library from Google
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
    Ember.$.getScript(this.get('url'));
    this.set('includedJs', true);
  },

  _loadingPromise: function() {
    var self = this;
    return new Ember.RSVP.Promise(function(resolve) {
      var wait = function() {
        if (typeof grecaptcha === "undefined") {
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
  },

  url: function() {
    return this.get('baseUrl') + '&hl=' + Ember.$('html').attr('lang');
  }.property('baseUrl'),

  refresh: function() {
    grecaptcha.reset();
  },

  value: function() {
    return grecaptcha.getResponse();
  }.property().volatile()
});
