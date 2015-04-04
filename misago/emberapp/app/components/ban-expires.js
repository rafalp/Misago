import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'p',
  isPermanent: Ember.computed.empty('model.expires_on'),

  expiresMoment: function() {
    if (!this.get('isPermanent')) {
      return moment.utc(this.get('model.expires_on'));
    } else {
      return null;
    }
  }.property('isPermanent'),

  expiresOn: function() {
    return this.get('expiresMoment');
  }.property('expiresMoment', 'clock.tick'),

  isExpired: function() {
    if (this.get('expiresOn')) {
      return moment().isAfter(this.get('expiresOn'));
    } else {
      return false;
    }
  }.property('isPermanent', 'expiresOn')
});
