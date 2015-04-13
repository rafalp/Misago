import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',
  classNames: 'form-horizontal',

  zxcvbn: Ember.inject.service('zxcvbn'),

  isReady: false,
  isErrored: false,
  isLoading: false,

  username: '',
  email: '',
  password: '',
  captcha: Ember.computed.alias('captcha.value'),

  validation: null,

  loadServices: function() {
    var self = this;

    var promises = [
      this.get('zxcvbn').load(),
      this.get('captcha').load()
    ];

    Ember.RSVP.allSettled(promises).then(function(array) {
      if (array[0].state === 'rejected') {
        self.set('isErrored', true);
        console.log('zxcvbn service failed to load.');
      }

      if (array[1].state === 'rejected') {
        self.set('isErrored', true);
        console.log('captcha service failed to load.');
      }

      self.set('isReady', !self.get('isErrored'));
    });
  }.on('didInsertElement'),

  submit: function() {
    if (this.get('isLoading')) {
      return false;
    }

    this.set('isLoading', true);

    var self = this;
    this.rpc.ajax('users', {
      username: this.get('username'),
      email: this.get('email'),
      password: this.get('password'),
      captcha: this.get('captcha.value')
    }).then(function(response) {
      self.success(response);
    }, function(jqXHR) {
        self.error(jqXHR);
    }).finally(function() {
      self.set('isLoading', false);
    })

    return false;
  },

  success: function(response) {
    console.log(response);
  },

  error: function(jqXHR) {
    if (jqXHR.status === 400) {
      this.set('validation', Ember.Object.create(jqXHR.responseJSON));
    }
  }
});
