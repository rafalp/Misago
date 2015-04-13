import DS from 'ember-data';

export default DS.Model.extend({
  question: DS.attr('string'),
  help_text: DS.attr('string')
});
