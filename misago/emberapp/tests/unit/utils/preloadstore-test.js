import PreloadStore from 'misago/utils/preloadstore';

module('PreloadStore');

test('has(key) method returns true for existing keys', function() {
  ok(PreloadStore.has('staticUrl'));
  ok(PreloadStore.has('mediaUrl'));
  ok(PreloadStore.has('misagoSettings'));
});

test('has(key) method returns false for undefined keys', function() {
  equal(PreloadStore.has('notExisting'), false);
});

test('get(key) method returns value for defined key', function() {
  equal(PreloadStore.get('misagoSettings'), window.MisagoData.misagoSettings);
  equal(PreloadStore.get('mediaUrl'), window.MisagoData.mediaUrl);
});

test('get(key) method returns undefined for undefined key', function() {
  equal(PreloadStore.get('undefinedKey'), undefined);
});

test('get(key, default) method returns default value for undefined key', function() {
  var key = 'undefinedKey';
  var defaultValue = 'Default value';

  equal(PreloadStore.get(key, defaultValue), defaultValue);
  ok(!PreloadStore.has(key));
});

test('get(key, default) method returns value for defined key', function() {
  var key = 'mediaUrl';

  equal(PreloadStore.get(key, 'Default Value'), window.MisagoData.mediaUrl);
  ok(PreloadStore.has(key));
});

test('set(key, value) method sets new value', function() {
  var key = 'testKey';

  var value = 'Lo Bob!';
  equal(PreloadStore.set(key, value), value);
  equal(PreloadStore.get(key), value);
  ok(PreloadStore.has(key));
});

test('pop(key, default) method returns default undefined for key', function() {
  var key = 'undefinedKey';
  var defaultValue = 'Default value';

  equal(PreloadStore.get(key, defaultValue), defaultValue);
  ok(!PreloadStore.has(key));
});

test('pop(key, default) method returns and deletes value for key', function() {
  var key = 'undefinedKey';
  var realValue = 'valid value!';
  var defaultValue = 'Default value';

  PreloadStore.set(key, realValue);

  equal(PreloadStore.pop(key, defaultValue), realValue);
  equal(PreloadStore.pop(key, defaultValue), defaultValue);
  ok(!PreloadStore.has(key));
});
