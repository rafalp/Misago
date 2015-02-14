import PreloadStore from '../../../utils/preloadstore';
import { module, test } from 'qunit';

module('PreloadStore');

test('has(key) method returns true for existing keys', function(assert) {
  assert.ok(PreloadStore.has('staticUrl'));
  assert.ok(PreloadStore.has('mediaUrl'));
  assert.ok(PreloadStore.has('misagoSettings'));
});

test('has(key) method returns false for undefined keys', function(assert) {
  assert.equal(PreloadStore.has('notExisting'), false);
});

test('get(key) method returns value for defined key', function(assert) {
  assert.equal(PreloadStore.get('misagoSettings'), window.MisagoData.misagoSettings);
  assert.equal(PreloadStore.get('mediaUrl'), window.MisagoData.mediaUrl);
});

test('get(key) method returns undefined for undefined key', function(assert) {
  assert.equal(PreloadStore.get('undefinedKey'), undefined);
});

test('get(key, default) method returns default value for undefined key', function(assert) {
  var key = 'undefinedKey';
  var defaultValue = 'Default value';

  assert.equal(PreloadStore.get(key, defaultValue), defaultValue);
  assert.ok(!PreloadStore.has(key));
});

test('get(key, default) method returns value for defined key', function(assert) {
  var key = 'mediaUrl';

  assert.equal(PreloadStore.get(key, 'Default Value'), window.MisagoData.mediaUrl);
  assert.ok(PreloadStore.has(key));
});

test('set(key, value) method sets new value', function(assert) {
  var key = 'testKey';
  var value = 'Lo Bob!';

  assert.equal(PreloadStore.set(key, value), value);
  assert.equal(PreloadStore.get(key), value);
  assert.ok(PreloadStore.has(key));
});

test('pop(key, default) method returns default undefined for key', function(assert) {
  var key = 'undefinedKey';
  var defaultValue = 'Default value';

  assert.equal(PreloadStore.get(key, defaultValue), defaultValue);
  assert.ok(!PreloadStore.has(key));
});

test('pop(key, default) method returns and deletes value for key', function(assert) {
  var key = 'undefinedKey';
  var realValue = 'valid value!';
  var defaultValue = 'Default value';

  PreloadStore.set(key, realValue);

  assert.equal(PreloadStore.pop(key, defaultValue), realValue);
  assert.equal(PreloadStore.pop(key, defaultValue), defaultValue);
  assert.ok(!PreloadStore.has(key));
});
