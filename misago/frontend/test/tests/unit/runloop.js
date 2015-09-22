(function () {
  'use strict';

  QUnit.module("RunLoop");

  var service = getMisagoService('runloop');

  QUnit.test("run", function(assert) {
    var container = {timesLeft: 5};
    var runloop = service.factory(container);

    var done = assert.async();

    runloop.run(function(_) {
      assert.ok(_.timesLeft, "#" + (6 - _.timesLeft) + ": runloop is called");
      _.timesLeft -= 1;

      if (_.timesLeft === 0) {
        assert.equal(runloop._intervals['test-loop'], null,
          "test loop was stopped");
        done();
        return false;
      } else if (_.timesLeft < 0) {
        assert.ok(false, 'runloop was not finished by false from function');
      }
    }, 'test-loop', 100);
  });

  QUnit.test("runOnce", function(assert) {
    var container = {};
    var runloop = service.factory(container);

    var ranOnce = assert.async();
    runloop.runOnce(function(_) {
      assert.equal(runloop._intervals['test-run-once'], null,
        "runloop item name was removed from intervals");

      assert.equal(container, _, "test task was ran with container");
      ranOnce();
    }, 'test-run-once', 80);

    assert.ok(runloop._intervals['test-run-once'],
      "runloop item name was added to intervals");

    var ranOnceOther = assert.async();
    runloop.runOnce(function(_) {
      assert.equal(runloop._intervals['test-run-once-other'], null,
        "runloop item name was removed from intervals");

      assert.equal(container, _, "other test task was ran with container");
      ranOnceOther();
    }, 'test-run-once-other', 100);

    assert.ok(runloop._intervals['test-run-once-other'],
      "runloop item name was added to intervals");
  });

  QUnit.test("stop", function(assert) {
    var container = {};
    var runloop = service.factory(container);

    runloop.run(function() {
      assert.ok(false, "runloop should be canceled before first run");
      return false;
    }, 'canceled-loop', 500);

    runloop.stop('canceled-loop');

    assert.equal(runloop._intervals['canceled-loop'], null,
      "stop canceled named loop");

    runloop.run(function() {
      assert.ok(false, "runloop should be canceled before first run");
      return false;
    }, 'other-canceled-loop', 500);

    runloop.stop();

    assert.equal(runloop._intervals['other-canceled-loop'], null,
      "stop canceled all loops");
  });
}());
