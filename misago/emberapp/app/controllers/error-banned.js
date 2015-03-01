import Ember from 'ember';

export default Ember.ObjectController.extend({
  isPermanent: function() {
    return this.get('model.expires_on') === null;
  }.property('model'),

  expiresMoment: function() {
    if (!this.get('isPermanent')) {
      return moment(this.get('model.expires_on'));
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
