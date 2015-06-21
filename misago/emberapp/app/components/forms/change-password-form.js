import Ember from 'ember';
import ValidatedForm from 'misago/components/forms/validated-form';

export default ValidatedForm.extend({
  tagName: 'form',
  classNames: 'form-horizontal',

  isBusy: false,

  new_password: '',
  repeat_password: '',
  password: '',

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/change-password';
  }.property(),

  newPasswordValidation: function() {
    var value = Ember.$.trim(this.get('new_password'));

    if (value.length === 0) {
      this.set('validation.new_password', [gettext('Enter new password.')]);
    } else if (value.length < this.get('settings.password_length_min')) {
      var limit = this.get('settings.password_length_min');
      var message = ngettext('Valid password must be at least %(limit)s character long.',
                             'Valid password must be at least %(limit)s characters long.',
                             limit);
      this.set('validation.new_password', [interpolate(message, {limit: limit}, true)]);
    } else {
      this.set('validation.new_password', 'ok');
    }
  }.observes('new_password', 'repeat_password'),

  repeatPasswordValidation: function() {
    var value = Ember.$.trim(this.get('repeat_password'));

    if (value.length === 0) {
      this.set('validation.repeat_password', [gettext('Repeat new password.')]);
    } else if (value !== Ember.$.trim(this.get('new_password'))) {
      this.set('validation.repeat_password', [gettext('Password differs from new password.')]);
    } else {
      this.set('validation.repeat_password', 'ok');
    }
  }.observes('new_password', 'repeat_password'),

  passwordValidation: function() {
    var value = Ember.$.trim(this.get('password'));

    if (value.length === 0) {
      this.set('validation.password', [gettext('Enter current password.')]);
    } else {
      this.set('validation.password', 'ok');
    }
  }.observes('password'),

  submit: function() {
    if (this.get('isBusy')) {
      return false;
    }

    var data = {
      new_password: Ember.$.trim(this.get('new_password')),
      repeat_password: Ember.$.trim(this.get('repeat_password')),
      password: Ember.$.trim(this.get('password')),
    };

    this.newPasswordValidation();
    this.repeatPasswordValidation();
    this.passwordValidation();

    if (this.hasValidationErrors()) {
      this.toast.error(gettext('Form contains errors.'));
      return false;
    }

    this.set('isBusy', true);

    var self = this;
    this.ajax.post(this.get('apiUrl'), data
    ).then(function(response) {
      if (self.isDestroyed) { return; }
      self.success(response);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      self.error(jqXHR);
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isBusy', false);
    });

    return false;
  },

  success: function(responseJSON) {
    this.setProperties({
      'new_password': '',
      'repeat_password': '',
      'password': '',
    });
    this.resetValidation();
    this.toast.info(responseJSON.detail);
  },

  error: function(jqXHR) {
    var rejection = jqXHR.responseJSON;
    if (jqXHR.status === 400) {
      this.toast.error(gettext('Form contains errors.'));
      this.get('validation').setProperties(rejection);
    } else {
      this.toast.apiError(jqXHR);
    }
  },
});
