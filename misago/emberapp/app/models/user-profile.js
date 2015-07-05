import DS from 'ember-data';
import SharedUserAttrs from 'misago/mixins/shared-user-attrs';

export default DS.Model.extend(SharedUserAttrs, {
  email: DS.attr('string'),
  acl: DS.attr('ember-object')
});
