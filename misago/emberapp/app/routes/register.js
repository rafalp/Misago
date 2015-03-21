import Ember from 'ember';
import MisagoRoute from 'misago/routes/misago';
import ResetScroll from 'misago/mixins/reset-scroll';

export default MisagoRoute.extend(ResetScroll, {
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

  stageTemplate: function() {
    return 'register.' + this.get('stage');
  }.property('stage'),

  renderTemplate: function() {
    this.resolveStage();
    this.render(this.get('stageTemplate'));
  },

  actions: {
    didTransition: function() {
      this.set('title', gettext("Register"));
    }
  }
});
