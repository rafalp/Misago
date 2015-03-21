import Ember from 'ember';

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
    this.setProperties({
      'username': '',
      'password': '',

      'isLoading': false,
      'showActivation': false
    });
  },

  actions: {
    open: function() {
      Ember.$('#loginModal').modal('show');
    },

    submit: function() {
      if (this.get('isLoading')) {
        return;
      }

      var credentials = {
        username: Ember.$.trim(this.get('username')),
        password: Ember.$.trim(this.get('password'))
      };

      if (!credentials.username || !credentials.password) {
        this.toast.warning(gettext("Fill out both fields."));
        return;
      }

      var self = this;
      this.rpc.ajax(this.get('settings.loginApiUrl'), credentials
      ).then(function() {
        self.send('success', credentials);
      }, function(jqXHR) {
        self.send('error', jqXHR);
      }).finally(function() {
        self.set('isLoading', false);
      });
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
        this.send('toastError', jqXHR);
      } else if (rejection.code === 'inactive_admin') {
        this.toast.info(rejection.detail);
      } else if (rejection.code === 'inactive_user') {
        this.toast.info(rejection.detail);
        this.set('showActivation', true);
      } else if (rejection.code === 'banned') {
        this.send('showBan', rejection.detail);
        Ember.run(function() {
          Ember.$('#loginModal').modal('hide');
        });
      } else {
        this.toast.error(rejection.detail);
      }
      return false;
    },

    // Go-to links

    activateAccount: function() {
      this.transitionToRoute('activation');
      Ember.$('#loginModal').modal('hide');
    },

    forgotPassword: function() {
      this.transitionToRoute('forgotten-password');
      Ember.$('#loginModal').modal('hide');
    }
  }
});
