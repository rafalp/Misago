import DRFSerializer from './drf';

export default DRFSerializer.extend({
  // Custom meta-data handling that's not discarding extra metadata
  // from api endpoints.
  extractMeta: function(store, type, payload) {
    if (payload && payload.results) {
      var meta = {};
      for(var k in payload) {
        if (k !== 'results') {
          meta[k] = payload[k];
        }
      }

      // Pass metadata to Ember store
      store.setMetadataFor(type, meta);
    }
  }
});
