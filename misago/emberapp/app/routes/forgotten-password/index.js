import Ember from 'ember';
import ResetScroll from 'misago/mixins/reset-scroll';

export default Ember.Route.extend(ResetScroll, {
  renderTemplate: function() {
    this.render('forgotten-password.request-link');
  },

  actions: {
    didTransition: function() {
      this.send('setTitle', gettext('Change forgotten password'));
      return true;
    },

    showSentPage: function(linkRecipient) {
      this.send('setTitle', gettext('Change password form link sent'));
      this.render('forgotten-password.link-sent', {
        model: linkRecipient
      });

      return true;
    },

    retry: function() {
      this.send('didTransition');
      this.renderTemplate();
      return true;
    }
  }
});
