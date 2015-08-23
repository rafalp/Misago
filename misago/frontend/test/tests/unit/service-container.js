(function () {
  'use strict';

  var container = null;

  QUnit.module("Service Container", {
    beforeEach: function() {
      container = new Misago();
      container._services = [];
    }
  });

  QUnit.test("addService registers service in container", function(assert) {
    assert.expect(2);

    var MockServiceFactory = function() {
      return null;
    };

    container.addService('test', MockServiceFactory);

    assert.equal(container._services.length, 1, "addService() registered single service in container");
    assert.equal(container._services[0].item, MockServiceFactory, "addService() registered MockServiceFactory service in container");
  });

  QUnit.test("service factories are called", function(assert) {
    assert.expect(1);

    var MockServiceFactory = function(_) {
      assert.ok(_, 'MockServiceFactory was called with container as argument.');
    };

    container._initServices([{name: 'test', item: MockServiceFactory}]);
  });

  QUnit.test("factories return values are set as context on container", function(assert) {
    assert.expect(1);

    var MockServiceFactory = function() {
      return 'ok!';
    };

    container._initServices([{name: 'test', item: MockServiceFactory}]);
    assert.equal(container.test, 'ok!', 'MockServiceFactory return value was set on container.');
  });

  QUnit.test("factories returning nothing don't set context on container", function(assert) {
    assert.expect(1);

    var MockServiceFactory = function() {
      'not returning anything';
    };

    container._initServices([{name: 'test', item: MockServiceFactory}]);
    assert.equal(container.test, undefined, "MockServiceFactory return value wasn't set on container.");
  });

  QUnit.test("services can be destroyed", function(assert) {
    assert.expect(2);

    var MockService = {
      factory: function(_) {
        assert.ok(_, "MockService's factory was called with container as argument.");
      },

      destroy: function(_) {
        assert.ok(_, "MockService's destroy was called with container as argument.");
      }
    };

    var services = [{name: 'test', item: MockService}];

    container._initServices(services);
    container._destroyServices(services);
  });

  QUnit.test("services are initialized and destroyed in right order", function(assert) {
    assert.expect(2);

    var initialization_order = [];
    var destruction_order = [];

    var services = [
      {
        name: 'test_1',
        item: {
          factory: function() {
            initialization_order.push(1);
          },

          destroy: function() {
            destruction_order.push(1);
          }
        }
      },
      {
        name: 'test_2',
        item: {
          factory: function() {
            initialization_order.push(2);
          },

          destroy: function() {
            destruction_order.push(2);
          }
        }
      }
    ];

    container._initServices(services);
    container._destroyServices(services);

    assert.deepEqual(initialization_order, [1, 2], 'services were initialized in right order.');
    assert.deepEqual(destruction_order, [2, 1], 'services were destroyed in right order.');
  });

  QUnit.test("initialization data is stored on container", function(assert) {
    assert.expect();

    container.init({outlet: 'test'});

    assert.equal(container.setup.outlet, 'test', 'container stored initialization data');
  });
}());
