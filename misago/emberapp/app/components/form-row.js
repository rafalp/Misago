import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'form-group',
  classNameBindings: [
    'hasFeedback:has-feedback',
    'hasSuccess:has-success',
    'hasError:has-error'
  ],

  hasFeedback: function() {
    return this.get('validation') !== null;
  }.property('validation'),

  hasSuccess: function() {
    return this.get('hasFeedback') && !this.get('hasError');
  }.property('hasFeedback', 'hasError'),

  hasError: function() {
    return this.get('hasFeedback') && this.get('errors');
  }.property('hasFeedback', 'errors'),

  errors: function() {
    if (this.get('hasFeedback')) {
      return this.get('validation.' + this.get('name')) || null;
    }

    return null;
  }.property('validation', 'name')

});
