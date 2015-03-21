import Ember from 'ember';

export default Ember.Object.extend({
  ajax: function(recordOrProcedure, dataOrProcedure, data) {
    // receive args
    var record = null;
    var procedure = null;

    if (arguments.length === 3) {
      record = recordOrProcedure;
      procedure = dataOrProcedure;
    } else {
      procedure = recordOrProcedure;
      data = dataOrProcedure;
    }

    // get adapter to be used for RPC
    // note: in case of Model being null this cheats adapterFor to return
    // 'adapter:application'. we are doing this, because for some reason
    // store.defaultAdapter fails to return django adapter
    var adapter = this.store.adapterFor(record || {typeKey: 'application'});

    // build api call URL
    var url = null;
    if (record) {
      url = this.buildRecordProcedureURL(adapter, record, procedure);
    } else {
      url = this.buildProcedureURL(adapter, procedure);
    }

    // return RPC promise
    return adapter.rpcAjax(url, data || null);
  },

  buildRecordProcedureURL: function(adapter, record, procedure) {
    var url = adapter.buildURL(record.typeKey, record.id, record);
    return url + '/' + Ember.String.camelize(procedure);
  },

  buildProcedureURL: function(adapter, procedure) {
    var url = adapter.buildURL(procedure);
    return this.unpluralizeUrlProcedure(url, procedure);
  },

  unpluralizeUrlProcedure: function(url, procedure) {
    // decamelize name and reverse path pluralization for type for procedure
    var decamelized = Ember.String.decamelize(procedure);
    var pluralized = Ember.String.pluralize(decamelized);

    return url.replace(pluralized, decamelized);
  }
});
