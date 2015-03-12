import Ember from 'ember';
import rpc from 'misago/utils/rpc';

export default Ember.ObjectController.extend({
  isLoading: false,
  password: '',

  actions: {
    changePassword: function() {
      if (this.get('isLoading')) {
        return;
      }

      var password = Ember.$.trim(this.get('password'));

      if (password === "") {
        this.get('toast').warning(gettext("Enter new password."));
        return;
      }

      this.set('isLoading', true);

      var self = this;
      rpc(this.get('change_password_url'), {
        password: password
      }).then(function() {
        self.set('password', '');

        self.send('openLoginModal');
        self.get('toast').success(gettext("Your password has been changed."));

      }, function(jqXHR) {
        var rejection = jqXHR.responseJSON;
        if (jqXHR.status === 400){
          self.get('toast').error(rejection.detail);
        } else {
          self.set('password', '');

          if (jqXHR.status === 404) {
            self.get('toast').error(rejection.detail);
            self.transitionTo('forgotten-password');
          } else {
            self.send("error", jqXHR);
          }
        }

      }).finally(function() {
        self.set('isLoading', false);
      });
    }
  }
});
