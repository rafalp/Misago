import DS from 'ember-data';
import WithUrlName from 'misago/mixins/with-url-name';

export default DS.Model.extend(WithUrlName, {
  name: DS.attr('string'),
  slug: DS.attr('string'),
  description: DS.attr('string'),
  css_class: DS.attr('string'),
  is_tab: DS.attr('boolean')
});
