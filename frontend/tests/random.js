import assert from 'assert';
import { int, range } from 'misago/utils/random';

describe('Randoms', function() {
  it("returns random int", function() {
    assert.ok(int(5, 10), "random number was returned");
  });

  it("returns random array", function() {
    assert.ok(range(5, 10).length, "random array was returned");
  });
});