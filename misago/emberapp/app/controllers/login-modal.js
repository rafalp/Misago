import Ember from 'ember';
import rpc from 'misago/utils/rpc';
import getCsrfToken from 'misago/utils/csrf';

export default Ember.Controller.extend({
  modal: null,

  isLoading: false,
  isBanned: false,
  showActivation: false,

  username: '',
  password: '',

  ban: null,

  scheduleSetup: function() {
    Ember.run.scheduleOnce('afterRender', this, this.setup);
  }.on('init'),

  setup: function() {
    this.modal = Ember.$('#loginModal').modal({show: false});

    this.modal.on('shown.bs.modal', function () {
      Ember.$('#loginModal').focus();
    });

    var self = this;
    this.modal.on('hidden.bs.modal', function() {
      self.reset();
    });
  },

  reset: function() {
    this.set('ban', null);

    this.set('username', '');
    this.set('password', '');

    this.set('isLoading', false);
    this.set('isBanned', false);
    this.set('showActivation', false);
  },

  isValid: function(credentials) {
    if (!credentials.username || !credentials.password) {
      this.send('flashWarning', gettext("Fill out both fields."));
      return false;
    }

    return true;
  },

  authenticate: function(credentials) {
    var self = this;
    rpc(this.get('settings.authApiUrl'), credentials).then(function() {
      self.logIn(credentials);
    }, function(rejection) {
      self.authError(rejection);
      self.set('isLoading', false);
    });
  },

  logIn: function(credentials) {
    var $form = Ember.$('#hidden-login-form');

    // we need to refresh CSRF token because previous api call changed it
    $form.find('input[name=csrfmiddlewaretoken]').val(getCsrfToken());

    // fill out form with user credentials and submit it, this will tell
    // misago to redirect user back to right page, and will trigger browser's
    // key ring feature
    $form.find('input[name=redirect_to]').val(window.location.href);
    $form.find('input[name=username]').val(credentials.username);
    $form.find('input[name=password]').val(credentials.password);
    $form.submit();
  },

  authError: function(rejection) {
    if (rejection.code === 'inactive_admin') {
      this.send('flashInfo', rejection.detail);
    } else if (rejection.code === 'inactive_user') {
      this.send('flashInfo', rejection.detail);
      this.set('showActivation', true);
    } else if (rejection.code === 'banned') {
      this.set('ban', rejection.detail);
      this.set('isBanned', true);
    } else {
      this.send('flashError', rejection.detail);
    }
  },

  actions: {
    open: function() {
      Ember.$('#loginModal').modal('show');
    },

    signIn: function() {
      if (!this.get('isLoading')) {
        var credentials = {
          username: Ember.$.trim(this.get('username')),
          password: Ember.$.trim(this.get('password'))
        };

        if (this.isValid(credentials)) {
          this.set('isLoading', true);
          this.authenticate(credentials);
        } else {
          this.set('isLoading', false);
        }
      }
    },
  }
});
