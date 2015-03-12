import Ember from 'ember';
import rpc from 'misago/utils/rpc';
import getCsrfToken from 'misago/utils/csrf';

export default Ember.Controller.extend({
  modal: null,

  isLoading: false,
  showActivation: false,

  username: '',
  password: '',

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
    this.set('username', '');
    this.set('password', '');

    this.set('isLoading', false);
    this.set('showActivation', false);
  },

  actions: {
    open: function() {
      Ember.$('#loginModal').modal('show');
    },

    signIn: function() {
      if (this.get('isLoading')) {
        return;
      }

      var credentials = {
        username: Ember.$.trim(this.get('username')),
        password: Ember.$.trim(this.get('password'))
      };

      if (!credentials.username || !credentials.password) {
        this.get('toast').warning(gettext("Fill out both fields."));
        return;
      }

      var self = this;
      rpc(this.get('settings.authApiUrl'), credentials
      ).then(function() {
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

      }, function(jqXHR) {
        var rejection = jqXHR.responseJSON;
        if (typeof rejection.code === "undefined") {
          self.send("error", rejection);
        } else {
          if (rejection.code === 'inactive_admin') {
            self.get('toast').info(rejection.detail);
          } else if (rejection.code === 'inactive_user') {
            self.get('toast').info(rejection.detail);
            self.set('showActivation', true);
          } else if (rejection.code === 'banned') {
            self.send('showBan', rejection.detail);
            Ember.run(function() {
              Ember.$('#loginModal').modal('hide');
            });
          } else {
            self.get('toast').error(rejection.detail);
          }
        }

      }).finally(function() {
        self.set('isLoading', false);
      });
    },

    forgotPassword: function() {
      this.transitionToRoute('forgotten-password');
      Ember.$('#loginModal').modal('hide');
    },

    activateAccount: function() {
      Ember.$('#loginModal').modal('hide');
    }
  }
});
