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

test('set(key, value) method sets new value', function() {
  var key = 'testKey';
  var value = 'Lo Bob!';
  equal(PreloadStore.set(key, value), value);
  equal(PreloadStore.get(key), value);
});
