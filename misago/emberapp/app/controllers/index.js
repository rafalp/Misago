import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    testInfo: function() {
      this.toast.info(this.get('newFlash'));
    },

    testSuccess: function() {
      this.toast.success(this.get('newFlash'));
    },

    testWarning: function() {
      this.toast.warning(this.get('newFlash'));
    },

    testError: function() {
      this.toast.error(this.get('newFlash'));
    }
  }
});
