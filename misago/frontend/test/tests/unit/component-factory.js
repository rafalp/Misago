(function () {
  'use strict';

  QUnit.module("Component factory");

  QUnit.test("service factory", function(assert) {
    var container = {};

    var service = getMisagoService('component-factory');
    service(container);

    assert.ok(container.component,
      "service factory has set component on container.");
  });
}());
