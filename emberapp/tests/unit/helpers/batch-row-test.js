import {
  batchRow
} from '../../../helpers/batch-row';
import { module, test } from 'qunit';

module('BatchRowHelper');

test('helper returns valid batches of list', function(assert) {
  assert.expect(7);

  var list = [];
  for (var i = 0; i < 48; i++) {
      list.push(i);
  }

  var batch = batchRow(list, 10);
  assert.equal(batch.length, 5);

  assert.equal(batch[2].length, 10);
  assert.equal(batch[2][0], 20);
  assert.equal(batch[2][9], 29);

  assert.equal(batch[4].length, 8);
  assert.equal(batch[4][0], 40);
  assert.equal(batch[4][7], 47);
});
