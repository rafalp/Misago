import Ember from 'ember';

export default Ember.Component.extend({
  showTermsLink: function() {
    return this.get('settings.terms_of_service') || this.get('settings.terms_of_service_link');
  }.property('settings'),

  showPrivacyLink: function() {
    return this.get('settings.privacy_policy') || this.get('settings.privacy_policy_link');
  }.property('settings'),

  hasContent: function() {
    return this.get('showTermsLink') || this.get('showPrivacyLink') || this.get('settings.forum_footnote');
  }.property('settings', 'showTermsLink', 'showPrivacyLink')
});
