(function (Misago) {
  'use strict';

  var Models = function() {
    this.classes = {};
    this.deserializers = {};
    this.relations = {};

    this.add = function(name, kwargs) {
      if (kwargs.class) {
        this.classes[name] = kwargs.class;
      }

      if (kwargs.deserialize) {
        this.deserializers[name] = kwargs.deserialize;
      }

      if (kwargs.relations) {
        for (var key in kwargs.relations) {
          if (kwargs.relations.hasOwnProperty(key)) {
            this.relations[name + ':' + key] = kwargs.relations[key];
          }
        }
      }
    };

    this.new = function(name, data) {
      if (this.classes[name]) {
        return new this.classes[name](data);
      } else {
        return data;
      }
    };

    this.deserialize = function(name, json) {
      if (this.relations[name]) {
        name = this.relations[name];
      }

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
