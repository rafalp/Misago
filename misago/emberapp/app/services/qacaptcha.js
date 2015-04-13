import Ember from 'ember';

export default Ember.Service.extend({
  field: 'qacaptcha-field',
  model: null,

  load: function() {
    // Obtain QA question from API
    var promise = this.store.find('captcha-question', 1);

    var self = this;
    promise.then(function(model) {
      self.set('model', model);
    });

    return promise;
  },

  value: function() {
    return Ember.$('#captcha-question').val() || '';
  }.property().volatile()
});
