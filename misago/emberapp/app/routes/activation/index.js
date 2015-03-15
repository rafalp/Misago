import Ember from 'ember';
import ResetScroll from 'misago/mixins/reset-scroll';

export default Ember.Route.extend(ResetScroll, {
  title: gettext('Request activation link'),
  templateName: 'activation.request-link',

  sentTitle: gettext('Activation link sent'),
  sentTemplateName: 'activation.link-sent',

  renderTemplate: function() {
    this.render(this.get('templateName'));
  },

  actions: {
    didTransition: function() {
      this.send('setTitle', this.get('title'));
      return true;
    },

    showSentPage: function(linkRecipient) {
      this.send('setTitle', this.get('sentTitle'));
      this.render(this.get('sentTemplateName'), {
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
