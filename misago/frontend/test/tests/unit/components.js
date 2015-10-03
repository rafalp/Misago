(function () {
  'use strict';

  QUnit.module("Components");

  QUnit.test("service factory", function(assert) {
    var container = {};

    var service = getMisagoService('components');
    service(container);

    assert.ok(container.component,
      "service factory has set component function on container.");
  });

  QUnit.test("component factory", function(assert) {
    var container = {};

    var service = getMisagoService('components');
    service(container);

    var view = function() {
      return 'ok!';
    };

    container.component('test-component', {
      view: view
    });

    assert.equal(container.component('test-component').view(), view(),
      "component service registered and constructed component.");
  });
}());
