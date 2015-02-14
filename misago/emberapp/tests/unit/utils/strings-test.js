import { startsWith, endsWith } from '../../../utils/strings';
import { module, test } from 'qunit';

module('strings');

test('startsWith works', function(assert) {
  assert.ok(startsWith("Boberson", "Bob"));
  assert.ok(!startsWith("Boberson", "bob"));
  assert.ok(!startsWith("Bob", "Boberson"));
});

test('endsWith works', function(assert) {
  assert.ok(endsWith("Boberson", "son"));
  assert.ok(!endsWith("Boberson", "Son"));
  assert.ok(!endsWith("Bob", "Boberson"));
});
