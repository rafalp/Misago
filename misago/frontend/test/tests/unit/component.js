(function (Misago) {
  'use strict';

  QUnit.module("Component factory");

  QUnit.test("service factory registers component() function on container", function(assert) {
    var container = {};
    Misago.ComponentFactory(container);

    assert.ok(container.component, "service has set component factory on container.");
  });
}(Misago.prototype));
