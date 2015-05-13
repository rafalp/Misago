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
  misagoAjax: function(method, url, data, onProgress) {
    var adapter = this;

    return new Ember.RSVP.Promise(function(resolve, reject) {
      var hash = adapter.ajaxOptions(url, method, {data: data || null});

      if (onProgress) {// if true we are uploading file
        // monitor progress
        hash.xhr = function() {
          var uploadingXhr = Ember.$.ajaxSettings.xhr();
          uploadingXhr.upload.addEventListener('progress', onProgress, false);
          return uploadingXhr;
        };

        // don't meddle with data
        hash.data = data;
        hash.contentType = false;
        hash.processData = false;
      }

      hash.success = function(json) {
        Ember.run(null, resolve, json);
      };

      hash.error = function(jqXHR) {
        Ember.run(null, reject, jqXHR);
      };

      Ember.$.ajax(hash);
    }, 'DS: MisagoAdapter#misago-ajax ' + method + ' to ' + url);
  }
});
