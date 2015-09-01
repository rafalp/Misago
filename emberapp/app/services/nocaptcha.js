import Ember from 'ember';

export default Ember.Service.extend({
  field: null,
  passed: false,

  load: function() {
    // CAPTCHA is turned off, so don't load anything
    return new Ember.RSVP.Promise(function(resolve) {
      resolve();
    });
  },

  value: function() {
    return '';
  }.property(),

  pass: function() {
    this.set('passed', true);
  },

  reset: function() {
    this.set('passed', false);
  },


  refresh: function() {
    return;
  }
});
