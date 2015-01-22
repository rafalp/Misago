import DS from 'ember-data';

export default DS.Model.extend({
  slug: DS.attr('slug'),
  title: DS.attr('string'),
  link: DS.attr('string'),
  body: DS.attr('string')
});
