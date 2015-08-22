(function (ns) {
  'use strict';

  var list = null;

  QUnit.module("OrderedList", {
    beforeEach: function() {
      list = new ns.OrderedList();
    }
  });

  QUnit.test("OrderedList stores and returns items", function(assert) {
    assert.equal(list.has('invalid_key'), false, "list.has() returned false for nonexisting key");

    list.add('valid_key', 'valid_value');
    assert.ok(list.has('valid_key'), "list.has() returned true for existing key");
    assert.equal(list.get('valid_key'), 'valid_value', "list.get() returned value for existing key");

    assert.equal(list.get('invalid_key', 'fallback'), 'fallback', "list.get() returned fallback value for nonexisting key");
  });

  QUnit.test("OrderedList orders and returns items", function(assert) {
    list.add('apple', 'apple');
    list.add('banana', 'banana');
    list.add('orange', 'orange');
    list.add('kiwi', 'kiwi', {before: 'banana'});
    list.add('melon', 'melon', {after: 'potato'});
    list.add('potato', 'potato');

    var unordered_list = list.values();

    assert.equal(list.is_ordered, false, "list.values() didn't set is_ordered flag on list");

    assert.equal(unordered_list[0], 'apple', 'unordered_list[0] is apple');
    assert.equal(unordered_list[1], 'banana', 'unordered_list[1] is banana');
    assert.equal(unordered_list[2], 'orange', 'unordered_list[2] is orange');
    assert.equal(unordered_list[3], 'kiwi', 'unordered_list[3] is kiwi');
    assert.equal(unordered_list[4], 'melon', 'unordered_list[4] is melon');
    assert.equal(unordered_list[5], 'potato', 'unordered_list[5] is potato');

    var ordered_list = list.order();

    assert.ok(list.is_ordered, "list.order() set is_ordered flag on list");

    assert.equal(ordered_list[0], 'apple', 'ordered_list[0] is apple');
    assert.equal(ordered_list[1], 'kiwi', 'ordered_list[1] is kiwi');
    assert.equal(ordered_list[2], 'banana', 'ordered_list[2] is banana');
    assert.equal(ordered_list[3], 'orange', 'ordered_list[3] is orange');
    assert.equal(ordered_list[4], 'potato', 'ordered_list[4] is potato');
    assert.equal(ordered_list[5], 'melon', 'ordered_list[5] is melon');
  });
}(Misago.prototype));
