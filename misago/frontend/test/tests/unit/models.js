(function () {
  'use strict';

  var service = getMisagoService('models');

  QUnit.module("Models");

  QUnit.test("service factory", function(assert) {
    var container = {};
    var models = service(container);

    assert.ok(models,
      "service factory has returned service instance.");
  });

  QUnit.test("add", function(assert) {
    var container = {};
    var models = service(container);

    var TestModel = function(data) {
      this.name = data.name || 'Hello';
    };

    var testModelDeserializer = function(data) {
      return data;
    };

    models.add('test-model', {
      class: TestModel,
      deserialize: testModelDeserializer
    });

    assert.equal(models.classes['test-model'], TestModel,
      "test model's class was registered in the service.");
    assert.equal(models.deserializers['test-model'], testModelDeserializer,
      "test model's deserializer was registered in the service.");
  });

  QUnit.test("new", function(assert) {
    var container = {};
    var models = service(container);

    var TestModel = function(data) {
      this.name = data.name || 'Hello';
    };

    models.add('test-model', {
      class: TestModel
    });

    var model = models.new('test-model', {name: 'Working!!!'});
    assert.equal(model.name, 'Working!!!',
      "new() returned model instance.");
  });

  QUnit.test("deserialize", function(assert) {
    var container = {};
    var models = service(container);

    var TestModel = function(data) {
      this.name = data.name;
    };

    var testModelDeserializer = function(data) {
      data.name = data.title;
      return data;
    };

    models.add('test-model', {
      class: TestModel,
      deserialize: testModelDeserializer
    });

    var model = models.deserialize('test-model', {title: 'Testing!'});
    assert.equal(model.name, 'Testing!',
      "deserialize() returned deserialized model instance.");

    models.add('other-model', {
      class: TestModel
    });

    model = models.deserialize('other-model', {name: 'Other!'});
    assert.equal(model.name, 'Other!',
      "deserialize() returned model instance without deserialization.");
  });
}());
