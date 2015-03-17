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
      this.get('page-title').setTitle(this.get('title'));
    },

    showSentPage: function(linkRecipient) {
      this.get('page-title').setTitle(this.get('sentTitle'));
      this.render(this.get('sentTemplateName'), {
        model: linkRecipient
      });
    },

    retry: function() {
      this.send('didTransition');
      this.renderTemplate();
    }
  }
});
