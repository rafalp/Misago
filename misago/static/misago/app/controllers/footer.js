Misago.FooterController = Ember.Controller.extend({
  showFooterTermsLink: function() {
    return this.get('settings.terms_of_service') || this.get('settings.terms_of_service_link');
  }.property('settings'),

  showFooterPrivacyLink: function() {
    return this.get('settings.privacy_policy') || this.get('settings.privacy_policy_link');
  }.property('settings'),

  showFooterNav: function() {
    return this.get('showFooterTermsLink') || this.get('showFooterPrivacyLink');
  }.property('showFooterTermsLink', 'showFooterPrivacyLink')
});
