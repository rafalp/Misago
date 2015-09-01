import Ember from 'ember';

export default Ember.Component.extend({
  validation: null,

  setValidation: function() {
    this.resetValidation();
  }.on('init'),

  resetValidation: function() {
    this.set('validation', Ember.Object.create({}));
  },

  hasValidationErrors: function() {
    var self = this;
    var hasErrors = false;

    Ember.keys(this.get('validation')).forEach(function(field) {
      if (self.get('validation.' + field) !== 'ok') {
        hasErrors = true;
      }
    });
    return hasErrors;
  }
});
