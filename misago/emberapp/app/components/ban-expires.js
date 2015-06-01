import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'p',
  isPermanent: Ember.computed.empty('model.expires_on'),

  expiresOn: function() {
    if (!this.get('isPermanent')) {
      return moment(this.get('model.expires_on'));
    } else {
      return null;
    }
  }.property('isPermanent', 'model.expires_on'),

  isExpired: function() {
    if (this.get('expiresOn')) {
      return moment().isAfter(this.get('expiresOn'));
    } else {
      return false;
    }
  }.property('isPermanent', 'expiresOn')
});
