import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return this.store.find('legal-page', 'privacy-policy');
  },

  actions: {
    didTransition: function() {
      this.send("setTitle", this.get('settings.privacy_policy_title') || gettext("Privacy policy"));
      return true;
    }
  }
});
