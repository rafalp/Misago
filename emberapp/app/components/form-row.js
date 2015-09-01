import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'form-group',
  classNameBindings: [
    'hasFeedback:has-feedback',
    'hasSuccess:has-success',
    'hasError:has-error'
  ],

  hasFeedback: function() {
    return typeof this.get('validation') !== 'undefined';
  }.property('validation'),

  hasSuccess: function() {
    return this.get('validation') === 'ok';
  }.property('hasFeedback'),

  hasError: function() {
    return this.get('hasFeedback') && !this.get('hasSuccess');
  }.property('hasFeedback', 'hasSuccess'),

  messages: function() {
    if (this.get('hasError')) {
      return this.get('validation');
    } else {
      return null;
    }
  }.property('hasError', 'hasSuccess')
});
