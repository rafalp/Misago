import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    logout: function() {
      this.auth.logout();
    }
  }
});
