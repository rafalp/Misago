import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    testInfo: function() {
      this.send('flashInfo', this.get('newFlash'));
    },

    testSuccess: function() {
      this.send('flashSuccess', this.get('newFlash'));
    },

    testWarning: function() {
      this.send('flashWarning', this.get('newFlash'));
    },

    testError: function() {
      this.send('flashError', this.get('newFlash'));
    }
  }
});
