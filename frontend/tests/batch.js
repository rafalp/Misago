import assert from 'assert';
import batch from 'misago/utils/batch';

describe('Batch', function() {
  it("splits list into batches", function() {
    assert.deepEqual(batch(['a', 'b', 'c', 'd', 'e'], 2), [
      ['a', 'b'], ['c', 'd'], ['e']
    ], "list was correctly batched");

    assert.deepEqual(batch(['a', 'b', 'c', 'd', 'e', 'f'], 2), [
      ['a', 'b'], ['c', 'd'], ['e', 'f']
    ], "list was correctly batched");

    assert.deepEqual(batch(['a', 'b', 'c', 'd', 'e', 'f'], 3), [
      ['a', 'b', 'c'], ['d', 'e', 'f']
    ], "list was correctly batched");
  });

  it("splits list into batches, pads them", function() {
    assert.deepEqual(batch(['a', 'b', 'c', 'd', 'e'], 2, '-'), [
      ['a', 'b'], ['c', 'd'], ['e', '-']
    ], "list was correctly batched and padded");

    assert.deepEqual(batch(['a', 'b', 'c', 'd', 'e', 'f'], 3, '-'), [
      ['a', 'b', 'c'], ['d', 'e', 'f']
    ], "list was correctly batched and padded");
  });
});