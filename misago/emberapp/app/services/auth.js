import Ember from 'ember';

export default Ember.Service.extend({
  isAnonymous: function() {
    return !this.get('isAuthenticated');
  }.property('isAuthenticated'),

  logout: function() {
    Ember.$('#hidden-logout-form').submit();
  },

  openLoginModal: function() {
    Ember.$('#loginModal').modal('show');
  }
});
