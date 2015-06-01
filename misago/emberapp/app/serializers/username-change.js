import DS from 'ember-data';
import DRFSerializer from './drf';

export default DRFSerializer.extend(DS.EmbeddedRecordsMixin, {
  attrs: {
    'user': { embedded: 'always' },
    'changed_by': { embedded: 'always' }
  }
});
