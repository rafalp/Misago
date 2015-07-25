import { updateObjProps, paginatedJSON } from '../../helpers/api-mocks';
import { module, test } from 'qunit';

module('api-mocks');

test('updateObjProps updates obj props', function(assert) {
  assert.expect(4);

  var testObj = { a: 123, b: { c: 123} };

  assert.equal(updateObjProps(testObj).a, 123);
  assert.ok(updateObjProps(testObj) !== testObj);
  assert.equal(updateObjProps(testObj, { b: 'test' }).a, 123);
  assert.equal(updateObjProps(testObj, { b: 'test' }).b, 'test');
});

test('paginatedJSON turns array into pagination response', function(assert) {
  assert.expect(49);

  var results = ['a', 'b', 'c', 'd', 'e', 'f'];
  assert.equal(paginatedJSON(results).results, results);

  var pagination = paginatedJSON(results, 12, 1, 8, 4);
  assert.equal(pagination.count, 12);
  assert.equal(pagination.pages, 1);
  assert.equal(pagination.next, null);
  assert.equal(pagination.last, null);
  assert.equal(pagination.previous, null);
  assert.equal(pagination.first, null);
  assert.equal(pagination.before, 0);
  assert.equal(pagination.more, 0);

  pagination = paginatedJSON(results, 20, 1, 8, 4);
  assert.equal(pagination.count, 20);
  assert.equal(pagination.pages, 2);
  assert.equal(pagination.next, null);
  assert.equal(pagination.last, 2);
  assert.equal(pagination.previous, null);
  assert.equal(pagination.first, null);
  assert.equal(pagination.before, 0);
  assert.equal(pagination.more, 12);

  pagination = paginatedJSON(results, 20, 2, 8, 4);
  assert.equal(pagination.count, 20);
  assert.equal(pagination.pages, 2);
  assert.equal(pagination.next, null);
  assert.equal(pagination.last, null);
  assert.equal(pagination.previous, null);
  assert.equal(pagination.first, 1);
  assert.equal(pagination.before, 8);
  assert.equal(pagination.more, 0);

  pagination = paginatedJSON(results, 30, 2, 8, 4);
  assert.equal(pagination.count, 30);
  assert.equal(pagination.pages, 4);
  assert.equal(pagination.next, 3);
  assert.equal(pagination.last, 4);
  assert.equal(pagination.previous, null);
  assert.equal(pagination.first, 1);
  assert.equal(pagination.before, 8);
  assert.equal(pagination.more, 14);

  pagination = paginatedJSON(results, 30, 3, 8, 4);
  assert.equal(pagination.count, 30);
  assert.equal(pagination.pages, 4);
  assert.equal(pagination.next, null);
  assert.equal(pagination.last, 4);
  assert.equal(pagination.previous, 2);
  assert.equal(pagination.first, 1);
  assert.equal(pagination.before, 16);
  assert.equal(pagination.more, 6);

  pagination = paginatedJSON(results, 20, 3, 6, 2);
  assert.equal(pagination.count, 20);
  assert.equal(pagination.pages, 3);
  assert.equal(pagination.next, null);
  assert.equal(pagination.last, null);
  assert.equal(pagination.previous, 2);
  assert.equal(pagination.first, 1);
  assert.equal(pagination.before, 12);
  assert.equal(pagination.more, 0);
});
