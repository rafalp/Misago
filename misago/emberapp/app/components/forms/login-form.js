import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'form',

  isLoading: false,
  showActivation: false,

  username: '',
  password: '',

  router: function() {
    return this.container.lookup('router:main');
  }.property(),

  submit: function() {
    if (this.get('isLoading')) {
      return false;
    }

    var credentials = {
      username: Ember.$.trim(this.get('username')),
      password: Ember.$.trim(this.get('password'))
    };

    if (!credentials.username || !credentials.password) {
      this.toast.warning(gettext("Fill out both fields."));
      return false;
    }

    var self = this;
    this.rpc.ajax(this.get('settings.loginApiUrl'), credentials
    ).then(function() {
      if (self.isDestroyed) { return; }
      self.success(credentials);
    }, function(jqXHR) {
      if (self.isDestroyed) { return; }
      self.error(jqXHR);
    }).finally(function() {
      if (self.isDestroyed) { return; }
      self.set('isLoading', false);
    });

    return false;
  },

  success: function(credentials) {
    var $form = Ember.$('#hidden-login-form');

    // refresh CSRF token because parent api call changed it
    this.csrf.updateFormToken($form);

    // fill out form with user credentials and submit it, this will tell
    // misago to redirect user back to right page, and will trigger browser's
    // key ring feature
    $form.find('input[name=redirect_to]').val(window.location.href);
    $form.find('input[name=username]').val(credentials.username);
    $form.find('input[name=password]').val(credentials.password);
    $form.submit();
  },

  error: function(jqXHR) {
    var rejection = jqXHR.responseJSON;
    if (jqXHR.status !== 400) {
      this.toast.apiError(jqXHR);
    } else if (rejection.code === 'inactive_admin') {
      this.toast.info(rejection.detail);
    } else if (rejection.code === 'inactive_user') {
      this.toast.info(rejection.detail);
      this.set('showActivation', true);
    } else if (rejection.code === 'banned') {
      this.get('router').intermediateTransitionTo('error-banned', rejection.detail);
      this.modal.hide();
    } else {
      this.toast.error(rejection.detail);
    }
  }
});
