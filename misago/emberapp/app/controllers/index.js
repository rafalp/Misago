import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    testInfo: function() {
      this.get('toast').info(this.get('newFlash'));
    },

    testSuccess: function() {
      this.get('toast').success(this.get('newFlash'));
    },

    testWarning: function() {
      this.get('toast').warning(this.get('newFlash'));
    },

    testError: function() {
      this.get('toast').error(this.get('newFlash'));
    }
  }
});
