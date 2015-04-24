import Ember from 'ember';

export default Ember.Service.extend({
  stage: 'form',

  isForm: Ember.computed.equal('stage', 'form'),
  isDone: Ember.computed.equal('stage', 'done'),
  isClosed: Ember.computed.equal('stage', 'closed'),

  resolveStage: function() {
    if (!this.get('isDone') && this.get('settings.account_activation') === 'closed') {
      // we didn't complete prior registration and registrations aren't open
      this.set('stage', 'closed');
    }
  },

  template: function() {
    return 'register.' + this.get('stage');
  }.property('stage')
});
