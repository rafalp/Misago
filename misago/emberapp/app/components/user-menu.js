import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'ul',
  classNames: ['dropdown-menu', 'user-dropdown', 'dropdown-menu-right'],
  ariaRole: 'menu',

  actions: {
    logout: function() {
      this.auth.logout();
    }
  }
});
