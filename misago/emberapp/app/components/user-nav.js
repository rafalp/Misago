import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['user-nav', 'navbar-right'],

  actions: {
    logout: function() {
      this.auth.logout();
    }
  }
});
