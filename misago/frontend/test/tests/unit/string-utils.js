(function (startsWith, endsWith) {
  'use strict';

  QUnit.module("String Utils");

  QUnit.test("startsWith", function(assert) {
    assert.expect(4);

    assert.ok(startsWith("Boberson", "Bob"),
      'found string at beginning of other string');
    assert.ok(!startsWith("Boberson", "bob"),
      'function is case sensitive');
    assert.ok(!startsWith("Bob", "Boberson"),
      'failed to find string at beginning of other string');
    assert.ok(!startsWith("", "Boberson"), 'tested empty string');
  });

  QUnit.test("endsWith", function(assert) {
    assert.expect(4);

    assert.ok(endsWith("Boberson", "son"),
      'found string at the end of other string');
    assert.ok(!endsWith("Boberson", "Son"), 'function is case sensitive');
    assert.ok(!endsWith("Bob", "Boberson"),
      'failed to find string at the end of other string');
    assert.ok(!endsWith("", "Boberson"), 'tested empty string');
  });
}(Misago.prototype.startsWith, Misago.prototype.endsWith));
