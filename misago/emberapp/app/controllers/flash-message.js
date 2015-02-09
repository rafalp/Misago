import Ember from 'ember';

export default Ember.Controller.extend({
  VISIBLE_FOR: 4500,
  HIDE_ANIMATION_LENGTH: 200,

  id: null,
  type: null,
  message: null,
  isVisible: false,

  isInfo: function() {
    return this.get('type') === 'info';
  }.property('type'),

  isSuccess: function() {
    return this.get('type') === 'success';
  }.property('type'),

  isWarning: function() {
    return this.get('type') === 'warning';
  }.property('type'),

  isError: function() {
    return this.get('type') === 'error';
  }.property('type'),

  showFlash: function(type, message) {
    var flashId = this.incrementProperty('id');
    this.set('type', type);
    this.set('message', message);
    this.set('isVisible', true);

    var self = this;
    Ember.run.later(function () {
      if (self.get('id') === flashId) {
        self.set('isVisible', false);
      }
    }, this.get('VISIBLE_FOR'));
  },

  actions: {
    setFlash: function(type, message) {
      var self = this;

      if (this.get('isVisible')) {
        this.set('isVisible', false);
        Ember.run.later(function () {
          self.showFlash(type, message);
        }, this.get('HIDE_ANIMATION_LENGTH'));
      } else {
        this.showFlash(type, message);
      }
    }
  }
});
