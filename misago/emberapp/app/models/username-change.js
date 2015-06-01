import DS from 'ember-data';

export default DS.Model.extend({
  user: DS.belongsTo('User'),
  changed_by: DS.belongsTo('User'),
  changed_by_username: DS.attr('string'),
  changed_by_slug: DS.attr('string'),
  changed_on: DS.attr('moment-date'),
  new_username: DS.attr('string'),
  old_username: DS.attr('string'),

  intId: function() {
    return + this.get('id');
  }.property('id')
});
