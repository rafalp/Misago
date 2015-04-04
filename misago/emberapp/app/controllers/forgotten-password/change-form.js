import Ember from 'ember';

export default Ember.ObjectController.extend({
  isLoading: false,
  password: '',

  change_password_url: function() {
    return 'change-password/' + this.get('user_id') + '/' + this.get('token');
  }.property('user_id', 'token'),

  actions: {
    submit: function() {
      if (this.get('isLoading')) {
        return;
      }

      var password = Ember.$.trim(this.get('password'));

      if (password === "") {
        this.toast.warning(gettext("Enter new password."));
        return;
      }

      this.set('isLoading', true);

      var self = this;
      this.rpc.ajax(this.get('change_password_url'), {
        password: password
      }).then(function() {
        self.send('success');
      }, function(jqXHR) {
        self.send('error', jqXHR);
      }).finally(function() {
        self.set('isLoading', false);
      });
    },

    success: function() {
      this.set('password', '');

      this.auth.openLoginModal();
      this.toast.success(gettext("Your password has been changed."));
    },

    error: function(jqXHR) {
      var rejection = jqXHR.responseJSON;
      if (jqXHR.status === 400){
        this.toast.error(rejection.detail);
      } else {
        if (jqXHR.status === 404) {
          this.toast.error(rejection.detail);
          this.transitionTo('forgotten-password');
        } else {
          this.toast.apiError(jqXHR);
        }
      }
    }
  }
});
