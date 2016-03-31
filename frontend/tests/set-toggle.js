import assert from 'assert';
import toggle from 'misago/utils/set-toggle';

describe("Set Toggle", function() {
  it("class api works", function() {
    let set = [];

    set = toggle(set, 2);
    assert.equal(set.length, 1, "array length changed");
    assert.equal(set[0], 2, "array contains toggled");

    set = toggle(set, 2);
    assert.equal(set.length, 0, "array was emptied");

    set = toggle(set, 2);
    assert.equal(set.length, 1, "array length changed");
    assert.equal(set[0], 2, "array contains toggled item again");
  });
});