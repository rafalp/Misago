import Ember from 'ember';
import DS from 'ember-data';
import WithUrlName from 'misago/mixins/with-url-name';

export default Ember.Mixin.create(WithUrlName, {
  username: DS.attr('string'),
  slug: DS.attr('string'),
  avatar_hash: DS.attr('string'),
  title: DS.attr('string'),
  rank: DS.attr('ember-object'),
  threads: DS.attr('number'),
  posts: DS.attr('number'),
  signature: DS.attr('string'),
  state: DS.attr('ember-object'),
  meta: DS.attr('ember-object'),

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
