import Ember from 'ember';
import ValidatedForm from 'misago/components/forms/validated-form';

export default ValidatedForm.extend({
  tagName: 'form',
  classNames: 'form-horizontal',

  isBusy: false,

  new_email: '',
  password: '',

  apiUrl: function() {
    return 'users/' + this.auth.get('user.id') + '/change-email';
  }.property(),

  newEmailValidation: function() {
    var value = Ember.$.trim(this.get('new_email'));
    var state = 'ok';

    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;

    if (value.length === 0) {
      state = [gettext('Enter new e-mail.')];
    } else if (value === this.get('auth.user.email')) {
      state = [gettext('New e-mail is same as current one.')];
    } else if (!re.test(value)) {
      state = [gettext('Invalid e-mail address.')];
    }

    this.set('validation.new_email', state);
  }.observes('new_email'),

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
      new_email: Ember.$.trim(this.get('new_email')),
      password: Ember.$.trim(this.get('password')),
    };

    this.newEmailValidation();
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
      'new_email': '',
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
