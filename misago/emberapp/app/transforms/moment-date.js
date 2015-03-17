import DS from 'ember-data';

export default DS.Transform.extend({
  deserialize: function(serialized) {
    return serialized ? serialized.format() : null;
  },

  serialize: function(deserialized) {
    return deserialized ? moment.utc(deserialized) : null;
  }
});
