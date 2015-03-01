import Ember from 'ember';
import rpc from 'misago/utils/rpc';

export default Ember.ObjectController.extend({
  isLoading: false,
  email: '',

  actions: {
    sendLink: function() {
      if (this.get('isLoading')) {
        return;
      }

      var email = Ember.$.trim(this.get('email'));

      if (email === "") {
        this.send('flashWarning', gettext("Enter e-mail address."));
        return;
      }

      this.set('isLoading', true);

      var self = this;
      rpc('change-password/send-link/', {
        email: email
      }).then(function(requestingUser) {
        self.send('showSentPage', requestingUser);
        self.set('email', '');

      }, function(jqXHR) {
        var rejection = jqXHR.responseJSON;

        if (jqXHR.status === 400){
          if (rejection.code === 'banned') {
            this.send('showBan', rejection.detail);
            this.set('email', '');
          } else {
            this.send('flashError', rejection.detail);
          }
        } else {
          self.send("error", jqXHR);
          self.set('email', '');
        }

      }).finally(function() {
        self.set('isLoading', false);
      });

      return false;
    }
  }
});
