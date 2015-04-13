import Ember from 'ember';

export default Ember.Component.extend({
  classNames: 'form-group',

  captcha: Ember.inject.service('qacaptcha'),
  model: Ember.computed.alias('captcha.model')
});
