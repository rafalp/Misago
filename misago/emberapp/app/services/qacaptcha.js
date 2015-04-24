import Ember from 'ember';
import NoCaptcha from 'misago/services/nocaptcha';

export default NoCaptcha.extend({
  field: 'qacaptcha-field',
  model: null,

  value: '',

  load: function() {
    // Obtain QA question from API
    var promise = this.store.find('captcha-question', 1);

    var self = this;
    promise.then(function(model) {
      self.set('model', model);
    });

    return promise;
  }
});
