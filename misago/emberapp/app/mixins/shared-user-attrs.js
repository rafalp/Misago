import Ember from 'ember';
import DS from 'ember-data';
import WithUrlName from 'misago/mixins/with-url-name';

export default Ember.Mixin.create(WithUrlName, {
  username: DS.attr('string'),
  slug: DS.attr('string'),
  avatar_hash: DS.attr('string'),
  title: DS.attr('string'),
  rank: DS.attr('ember-object'),
  state: DS.attr('ember-object'),
  signature: DS.attr('string'),

  finalTitle: function() {
    if (this.get('title')) {
      return this.get('title');
    } else if (this.get('rank.title')) {
      return this.get('rank.title');
    } else {
      return '';
    }
  }.property('title', 'rank.title')
});
