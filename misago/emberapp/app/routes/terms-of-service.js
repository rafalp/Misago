import Ember from 'ember';

export default Ember.Route.extend({
  model: function() {
    return this.store.find('legal-page', 'terms-of-service');
  },

  actions: {
    didTransition: function() {
      this.send("setTitle", this.get('settings.terms_of_service_title') || gettext("Terms of service"));
      return true;
    }
  }
});
