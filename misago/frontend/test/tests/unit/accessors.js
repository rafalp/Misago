(function (ns) {
  'use strict';

  QUnit.module("Accessors");

  QUnit.test("Misago.has accessor", function(assert) {
    var test_obj = {valid: 'okay'};

    assert.equal(ns.has(test_obj, 'invalid'), false, "Misago.has() returned false for nonexisting key");
    assert.equal(ns.has(test_obj, 'valid'), true, "Misago.has() returned true for existing key");
  });

  QUnit.test("Misago.get accessor", function(assert) {
    var test_obj = {valid: 'okay'};

    assert.equal(ns.get(test_obj, 'invalid'), undefined, "Misago.get() returned undefined for nonexisting key");
    assert.equal(ns.get(test_obj, 'invalid', 'fallback'), 'fallback', "Misago.get() returned fallback value for nonexisting key");
    assert.equal(ns.get(test_obj, 'valid'), 'okay', "Misago.get() returned value for existing key");
    assert.equal(ns.get(test_obj, 'valid', 'fallback'), 'okay', "Misago.get() returned value for existing key instead of fallback");
  });

  QUnit.test("Misago.pop accessor", function(assert) {
    var test_obj = {valid: 'okay', other_valid: 'okay'};

    assert.equal(ns.pop(test_obj, 'invalid'), undefined, "Misago.pop() returned undefined for nonexisting key");
    assert.equal(ns.pop(test_obj, 'invalid', 'fallback'), 'fallback', "Misago.pop() returned fallback value for nonexisting key");
    assert.equal(ns.pop(test_obj, 'valid'), 'okay', "Misago.pop() returned value for existing key");
    assert.equal(ns.pop(test_obj, 'other_valid', 'fallback'), 'okay', "Misago.pop() returned value for existing key instead of fallback");

    assert.equal(ns.has(test_obj, 'valid'), false, "Misago.pop() removed valid key from object");
    assert.equal(ns.has(test_obj, 'other_valid'), false, "Misago.pop() removed other valid key from object");
  });
}(Misago.prototype));
