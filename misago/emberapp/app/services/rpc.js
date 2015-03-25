import Ember from 'ember';

export default Ember.Service.extend({
  ajax: function(recordOrProcedure, dataOrProcedure, data) {
    // unpack arguments
    var record = null;
    var procedure = null;

    if (typeof recordOrProcedure === 'string') {
      procedure = recordOrProcedure;
      data = dataOrProcedure;
    } else {
      record = recordOrProcedure;
      procedure = dataOrProcedure;
    }

    var model = null;
    if (record) {
      model = this.store.modelFor(record.constructor);
    }

    // get adapter to be used for RPC
    // note: in case of Model being null this cheats adapterFor to return
    // 'adapter:application'. we are doing this, because for some reason
    // store.defaultAdapter fails to return django adapter
    var adapter = this.store.adapterFor(model || {typeKey: 'application'});

    // build api call URL
    var url = null;
    if (record) {
      url = this.buildRecordProcedureURL(adapter, model, record, procedure);
    } else {
      url = this.buildProcedureURL(adapter, procedure);
    }

    // return RPC promise
    return adapter.rpcAjax(url, data || null);
  },

  buildRecordProcedureURL: function(adapter, model, record, procedure) {
    var url = adapter.buildURL(model.typeKey, record.id, record);
    var procedureSegment = Ember.String.decamelize(procedure).replace('_', '-');

    return url + procedureSegment + '/';
  },

  buildProcedureURL: function(adapter, procedure) {
    var url = adapter.buildURL(procedure);
    return this.unpluralizeUrlProcedure(url, procedure);
  },

  unpluralizeUrlProcedure: function(url, procedure) {
    // decamelize name and reverse path pluralization for type for procedure
    var decamelized = Ember.String.decamelize(procedure).replace('_', '-');
    var pluralized = Ember.String.pluralize(decamelized);

    return url.replace(pluralized, decamelized);
  }
});
