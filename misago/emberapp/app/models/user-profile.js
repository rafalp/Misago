import DS from 'ember-data';
import SharedUserAttrs from 'misago/mixins/shared-user-attrs';

export default DS.Model.extend(SharedUserAttrs, {
  acl: DS.attr('ember-object')
});
