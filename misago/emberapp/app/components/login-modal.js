import Ember from 'ember';

export default Ember.Component.extend({
  modal: null,

  isLoading: false,
  showActivation: false,

  username: '',
  password: '',

  router: function() {
    return this.container.lookup('router:main');
  }.property(),

  setup: function() {
    this.modal = Ember.$('#loginModal').modal({show: false});

    this.modal.on('shown.bs.modal', function () {
      Ember.$('#loginModal').focus();
    });

    var self = this;
    this.modal.on('hidden.bs.modal', function() {
      self.reset();
    });
  }.on('didInsertElement'),

  reset: function() {
    this.setProperties({
      'username': '',
      'password': '',

      'isLoading': false,
      'showActivation': false
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

  toastError: 'toastError',
  showBan: 'showBan',

  error: function(jqXHR) {
    var rejection = jqXHR.responseJSON;
    if (jqXHR.status !== 400) {
      this.sendAction('toastError', jqXHR);
    } else if (rejection.code === 'inactive_admin') {
      this.toast.info(rejection.detail);
    } else if (rejection.code === 'inactive_user') {
      this.toast.info(rejection.detail);
      this.set('showActivation', true);
    } else if (rejection.code === 'banned') {
      this.sendAction('showBan', rejection.detail);
      Ember.run(function() {
        Ember.$('#loginModal').modal('hide');
      });
    } else {
      this.toast.error(rejection.detail);
    }
  },

  actions: {
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
        self.success(credentials);
      }, function(jqXHR) {
        self.error(jqXHR);
      }).finally(function() {
        self.set('isLoading', false);
      });
    },

    // Go-to links

    activateAccount: function() {
      this.get('router').transitionTo('activation');
      Ember.$('#loginModal').modal('hide');
    },

    forgotPassword: function() {
      this.get('router').transitionTo('forgotten-password');
      Ember.$('#loginModal').modal('hide');
    }
  }
});
