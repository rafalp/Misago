import Ember from 'ember';
import FormRow from 'misago/components/form-row';

export default FormRow.extend({
  classNames: ['form-group', 'form-captcha'],
  captcha: Ember.inject.service('qacaptcha'),
  model: Ember.computed.alias('captcha.model'),

  value: '',

  syncWithService: function() {
    this.get('captcha').set('value', this.get('value'));
  }.observes('value')
});
