import Ember from 'ember';

export default Ember.Service.extend({
  get: function(recordOrProperty, recordProperty) {
    if (typeof recordOrProperty === 'string' || typeof recordProperty !== 'string') {
      recordProperty = null;
    }

    return this._ajax('GET', recordOrProperty, recordProperty);
  },

  post: function(recordOrProcedure, dataOrProcedure, data) {
    return this._ajax('POST', recordOrProcedure, dataOrProcedure, data);
  },

  _ajax: function(method, recordOrProcedure, dataOrProcedure, data) {
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

    // get adapter to be used for ajax
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

    // return promise
    return adapter.misagoAjax(method, url, data || null);
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
