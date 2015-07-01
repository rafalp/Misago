import Ember from 'ember';
import DS from 'ember-data';

export default DS.Transform.extend({
  deserialize: function(deserialized) {
    return Ember.Object.create(deserialized || {});
  },

  serialize: function(serialized) {
    return serialized;
  }
});
