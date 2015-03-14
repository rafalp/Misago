import Ember from 'ember';
import rpc from 'misago/utils/rpc';

export default Ember.ObjectController.extend({
  isLoading: false,
  email: '',

  actions: {
    submit: function() {
      if (this.get('isLoading')) {
        return;
      }

      var email = Ember.$.trim(this.get('email'));

      if (email === "") {
        this.get('toast').warning(gettext("Enter e-mail address."));
        return;
      }

      this.set('isLoading', true);

      var self = this;
      rpc('change-password/send-link/', {
        email: email
      }).then(function(requestingUser) {
        self.send('success', requestingUser);
      }, function(jqXHR) {
        self.send('error', jqXHR);
      }).finally(function() {
        self.set('isLoading', false);
      });
    },

    success: function(requestingUser) {
      this.send('showSentPage', requestingUser);
      this.set('email', '');
    },

    error: function(jqXHR) {
      if (jqXHR.status === 400){
        var rejection = jqXHR.responseJSON;
        if (rejection.code === 'banned') {
          this.send('showBan', rejection.detail);
          this.set('email', '');
        } else {
          this.get('toast').error(rejection.detail);
        }
      } else {
        this.send('toastError', jqXHR);
      }
    }
  }
});
