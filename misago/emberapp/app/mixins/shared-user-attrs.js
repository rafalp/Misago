import DS from 'ember-data';
import WithUrlName from 'misago/mixins/with-url-name';

export default Ember.Mixin.create(WithUrlName, {
  username: DS.attr('string'),
  slug: DS.attr('string'),
  avatar_hash: DS.attr('string'),
  title: DS.attr('string'),
  rank: DS.attr('ember-object'),
  state: DS.attr('string'),
  signature: DS.attr('ember-object')
});
