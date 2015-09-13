(function () {
  'use strict';

  QUnit.module("Component factory");

  QUnit.test("service factory registers component() function on container", function(assert) {
    var container = {};

    var service = getMisagoService('component-factory');
    service(container);

    assert.ok(container.component, "service has set component factory on container.");
  });
}());
