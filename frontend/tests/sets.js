import assert from 'assert';
import { push, remove, toggle } from 'misago/utils/sets';

describe("Sets Utils", function() {
  it("push", function() {
    let set = [];

    set = push(set, 2);
    assert.equal(set.length, 1, "array length changed");
    assert.equal(set[0], 2, "array contains pushed value");

    set = push(set, 2);
    assert.equal(set.length, 1, "array length didn't change");
    assert.equal(set[0], 2, "array contains pushed value");

    set = push(set, 1);
    assert.equal(set.length, 2, "array length changed");
    assert.equal(set[0], 2, "array contains original item");
    assert.equal(set[1], 1, "array contains pushed item");
  });

  it("remove", function() {
    let set = [1, 2, 3];

    set = remove(set, 2);
    assert.equal(set.length, 2, "array length changed");
    assert.equal(set[1], 3, "removed value is no longer in array");

    set = remove(set, 2);
    assert.equal(set.length, 2, "array length didn't change");
  });

  it("toggle", function() {
    let set = [];

    set = toggle(set, 2);
    assert.equal(set.length, 1, "array length changed");
    assert.equal(set[0], 2, "array contains toggled value");

    set = toggle(set, 2);
    assert.equal(set.length, 0, "array was emptied");

    set = toggle(set, 2);
    assert.equal(set.length, 1, "array length changed");
    assert.equal(set[0], 2, "array contains toggled item again");
  });
});