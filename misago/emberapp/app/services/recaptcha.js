import Ember from 'ember';

export default Ember.Service.extend({
  field: 'recaptha-field',

  load: function() {
    // Load reCaptcha library from Google
    return new Ember.RSVP.Promise(function(resolve) {
      resolve();
    });
  },

  value: function() {
    return '';
  }.property().volatile()
});
