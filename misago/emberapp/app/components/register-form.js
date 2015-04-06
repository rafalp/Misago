import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',

  zxcvbn: Ember.inject.service('zxcvbn'),

  isReady: false,
  isLoading: false,
  password: '',

  loadZxcvb: function() {
    var self = this;
    this.get('zxcvbn').loadLibrary().then(function() {
      self.set('isReady', true);
      console.log(self.get('zxcvbn').testPassword('pass1234'));
    });
  }.on('didInsertElement'),

  submit: function() {
    return false;
  }
});
