import Ember from 'ember';
import DRFAdapter from './drf';

export default DRFAdapter.extend({
  headers: function() {
    return {
      'X-CSRFToken': this.get('csrf.token')
    };
  }.property().volatile(),

  // Simple ajax util for RPC requests
  // raison d'etre: because default ones are processing server responses
  // and there isn't response standard to allow that for RPC's
  rpcAjax: function(url, data) {
    var adapter = this;

    return new Ember.RSVP.Promise(function(resolve, reject) {
      var hash = adapter.ajaxOptions(url, 'POST', {data: data || null});

      hash.success = function(json) {
        Ember.run(null, resolve, json);
      };

      hash.error = function(jqXHR) {
        Ember.run(null, reject, jqXHR);
      };

      Ember.$.ajax(hash);
    }, 'DS: MisagoAdapter#rpc-ajax POST to ' + url);
  }
});
