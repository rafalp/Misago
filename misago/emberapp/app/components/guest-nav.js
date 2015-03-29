import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['guest-nav', 'navbar-right'],

  router: function() {
    return this.container.lookup('router:main');
  }.property(),

  actions: {
    login: function() {
      this.auth.openLoginModal();
    },

    register: function() {
      this.get('router').transitionTo('register');
    }
  }
});
