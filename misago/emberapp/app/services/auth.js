import Ember from 'ember';

export default Ember.Object.extend({
  isAnonymous: function() {
    return !this.get('isAuthenticated');
  }.property('isAuthenticated'),

  logout: function() {

  }
});
