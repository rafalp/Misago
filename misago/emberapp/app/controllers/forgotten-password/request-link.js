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
        if (jqXHR.status === 400){
          var rejection = jqXHR.responseJSON;
          if (rejection.code === 'banned') {
            self.send('showBan', rejection.detail);
            self.set('email', '');
          } else {
            self.send('flashError', rejection.detail);
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
