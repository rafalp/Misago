import DS from 'ember-data';

export default DS.Transform.extend({
  deserialize: function(deserialized) {
    return deserialized ? moment(deserialized) : null;
  },

  serialize: function(serialized) {
    return serialized ? serialized.format() : null;
  }
});
