(function () {
  'use strict';

  var container = null;

  var MockServiceFactory = function() {
    return null;
  };

  QUnit.module("Service Container", {
    beforeEach: function() {
      container = new Misago();
      container._services = [];
    }
  });

  QUnit.test("addService registers service in container", function(assert) {
    container.addService('test', MockServiceFactory);

    assert.equal(container._services.length, 1, "addService() registered single service in container");
    assert.equal(container._services[0].item, MockServiceFactory, "addService() registered MockServiceFactory service in container");
  });
}());
