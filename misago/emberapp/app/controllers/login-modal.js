import Ember from 'ember';
import MisagoPreloadStore from 'misago/utils/preloadstore';
import rpc from 'misago/utils/rpc';

export default Ember.Controller.extend({
  modal: null,

  message: '',

  username: '',
  password: '',

  isLoading: false,
  showActivation: false,

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
    this.set('message', '');

    this.set('username', '');
    this.set('password', '');

    this.set('isLoading', false);
    this.set('showActivation', false);
  },

  isValid: function(credentials) {
    this.set('isLoading', true);

    if (!credentials.username || !credentials.password) {
      this.send('flashWarning', gettext("Fill out both fields."));
      return false;
    }

    return true;
  },

  authenticate: function(credentials) {
    var self = this;
    rpc(MisagoPreloadStore.get('authApiUrl'), credentials).then(function() {
      self.logIn(credentials);
    }, function(rejection) {
      self.authError(rejection);
    }).finally(function() {
      self.set('isLoading', false);
    });
  },

  logIn: function(credentials) {
    this.send('flashSuccess', gettext("You are authenticated!"));
    console.log(credentials);
  },

  authError: function(rejection) {
    if (rejection.code === 'inactive_admin') {
      this.send('flashInfo', rejection.detail);
    } else if (rejection.code === 'inactive_user') {
      this.send('flashInfo', rejection.detail);
      this.set('showActivation', true);
    } else if (rejection.code === 'banned') {
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
          this.authenticate(credentials);
        } else {
          this.set('isLoading', false);
        }
      }
    }
  }
});
