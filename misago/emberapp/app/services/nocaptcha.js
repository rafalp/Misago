import Ember from 'ember';

export default Ember.Service.extend({
  field: null,

  load: function() {
    // CAPTCHA is turned off, so don't load anything
    return new Ember.RSVP.Promise(function(resolve) {
      resolve();
    });
  },

  value: function() {
    return '';
  }.property()
});
