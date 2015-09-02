(function (Misago) {
  'use strict';

  QUnit.module("Accessors");

  QUnit.test("Misago.has accessor", function(assert) {
    var testObj = {valid: 'okay'};

    assert.equal(Misago.has(testObj, 'invalid'), false, "Misago.has() returned false for nonexisting key");
    assert.equal(Misago.has(testObj, 'valid'), true, "Misago.has() returned true for existing key");
  });

  QUnit.test("Misago.get accessor", function(assert) {
    var testObj = {valid: 'okay'};

    assert.equal(Misago.get(testObj, 'invalid'), undefined, "Misago.get() returned undefined for nonexisting key");
    assert.equal(Misago.get(testObj, 'invalid', 'fallback'), 'fallback', "Misago.get() returned fallback value for nonexisting key");
    assert.equal(Misago.get(testObj, 'valid'), 'okay', "Misago.get() returned value for existing key");
    assert.equal(Misago.get(testObj, 'valid', 'fallback'), 'okay', "Misago.get() returned value for existing key instead of fallback");
  });

  QUnit.test("Misago.pop accessor", function(assert) {
    var testObj = {valid: 'okay', other_valid: 'okay'};

    assert.equal(Misago.pop(testObj, 'invalid'), undefined, "Misago.pop() returned undefined for nonexisting key");
    assert.equal(Misago.pop(testObj, 'invalid', 'fallback'), 'fallback', "Misago.pop() returned fallback value for nonexisting key");
    assert.equal(Misago.pop(testObj, 'valid'), 'okay', "Misago.pop() returned value for existing key");
    assert.equal(Misago.pop(testObj, 'other_valid', 'fallback'), 'okay', "Misago.pop() returned value for existing key instead of fallback");

    assert.equal(Misago.has(testObj, 'valid'), false, "Misago.pop() removed valid key from object");
    assert.equal(Misago.has(testObj, 'other_valid'), false, "Misago.pop() removed other valid key from object");
  });
}(Misago.prototype));
