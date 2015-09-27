(function () {
  'use strict';

  QUnit.module("Acceptance Tests Utils");

  QUnit.test("create and destroy Misago app", function(assert) {
    var done = assert.async();
    var app = initTestMisago();

    assert.equal($('#router-fixture').length, 1, "#router-fixture created");

    app.destroy();

    window.setTimeout(function() {
      assert.equal($('#router-fixture').length, 0, "#router-fixture removed");
      done();
    }, 100);
  });
}());
