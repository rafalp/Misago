import {
  fromNow
} from '../../../helpers/from-now';
import { module, test } from 'qunit';

module('FromNowHelper');

test('helper returns valid from now', function(assert) {
  var teststamp = moment();
  teststamp.add(7, 'days');

  var result = fromNow(teststamp);
  assert.equal(result, "in 7 days");

  result = fromNow(teststamp, {hash: {nosuffix: true}});
  assert.equal(result, "7 days");
});
