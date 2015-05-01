import Ember from 'ember';

export default Ember.Service.extend({
  isAnonymous: Ember.computed.not('isAuthenticated'),

  logout: function() {
    Ember.$('#hidden-logout-form').submit();
  },

  blockAuthenticated: function(message) {
    // TODO: if user is authenticated, throw error 403 with message
  },

  blockAnonymous: function(message) {
    // TODO: if user is not authenticated, throw error 403 with message
  }
});
