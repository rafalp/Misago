import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'li',
  classNames: ['user-menu', 'dropdown'],

  actions: {
    logout: function() {
      this.auth.logout();
    }
  }
});
