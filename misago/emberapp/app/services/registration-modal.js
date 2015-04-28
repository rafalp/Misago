import Ember from 'ember';

export default Ember.Service.extend({
  stage: 'form',

  isForm: Ember.computed.equal('stage', 'form'),
  isClosed: Ember.computed.equal('stage', 'closed'),

  resolveStage: function() {
    if (this.get('settings.account_activation') === 'closed') {
      // we didn't complete prior registration and registrations aren't open
      this.set('stage', 'closed');
    }
  }.on('init'),

  template: function() {
    return 'register.' + this.get('stage');
  }.property('stage')
});
