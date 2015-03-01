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
        this.send('flashWarning', gettext("Enter new password."));
        return;
      }

      this.set('isLoading', true);

      var self = this;
      rpc(this.get('change_password_url'), {
        password: password
      }).then(function() {
        self.set('password', '');

        self.send('openLoginModal');
        self.send('flashSuccess', gettext("Your password has been changed."));

      }, function(jqXHR) {
        if (jqXHR.status === 400){
          this.send('flashError', jqXHR.responseJSON.detail);
        } else {
          self.set('password', '');

          if (jqXHR.status === 404) {
            self.send('flashError', rejection.detail);
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
