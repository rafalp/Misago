(function (Misago) {
  'use strict';

  var Models = function() {
    this.classes = {};
    this.deserializers = {};

    this.add = function(name, kwargs) {
      if (kwargs.class) {
        this.classes[name] = kwargs.class;
      }

      if (kwargs.deserialize) {
        this.deserializers[name] = kwargs.deserialize;
      }
    };

    this.new = function(name, data) {
      if (this.classes[name]) {
        // Coerce ID to string
        // This is done to avoid type comparisions gotchas
        // later into app
        data.id = data.id ? String(data.id) : null;

        return new this.classes[name](data);
      } else {
        return data;
      }
    };

    this.deserialize = function(name, json) {
      if (this.deserializers[name]) {
        return this.new(name, this.deserializers[name](json, this));
      } else {
        return this.new(name, json);
      }
    };
  };

  Misago.addService('models', function() {
    return new Models();
  });
}(Misago.prototype));
