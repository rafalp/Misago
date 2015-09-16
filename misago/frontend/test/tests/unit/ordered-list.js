(function (Misago) {
  'use strict';

  var list = null;

  QUnit.module("OrderedList", {
    beforeEach: function() {
      list = new Misago.OrderedList();
    }
  });

  QUnit.test("OrderedList stores and returns items", function(assert) {
    assert.equal(list.has('invalid_key'), false,
      "list.has() returned false for nonexisting key");

    list.add('valid_key', 'valid_value');
    assert.ok(list.has('valid_key'),
      "list.has() returned true for existing key");
    assert.equal(list.get('valid_key'), 'valid_value',
      "list.get() returned value for existing key");

    assert.equal(list.get('invalid_key', 'fallback'), 'fallback',
      "list.get() returned fallback value for nonexisting key");
  });

  QUnit.test("OrderedList orders and returns items", function(assert) {
    list.add('apple', 'apple');
    list.add('banana', 'banana');
    list.add('orange', 'orange');
    list.add('lichi', 'lichi', {before: '_end'});
    list.add('kiwi', 'kiwi', {before: 'banana'});
    list.add('melon', 'melon', {after: 'potato'});
    list.add('potato', 'potato');

    var unorderedList = list.values();

    assert.equal(list.isOrdered, false,
      "list.values() didn't set isOrdered flag on list");

    assert.equal(unorderedList[0], 'apple', 'unorderedList[0] is apple');
    assert.equal(unorderedList[1], 'banana', 'unorderedList[1] is banana');
    assert.equal(unorderedList[2], 'orange', 'unorderedList[2] is orange');
    assert.equal(unorderedList[3], 'lichi', 'unorderedList[3] is lichi');
    assert.equal(unorderedList[4], 'kiwi', 'unorderedList[4] is kiwi');
    assert.equal(unorderedList[5], 'melon', 'unorderedList[5] is melon');
    assert.equal(unorderedList[6], 'potato', 'unorderedList[6] is potato');

    var orderedList = list.order();

    assert.ok(list.isOrdered, "list.order() set isOrdered flag on list");

    assert.equal(orderedList[0], 'apple', 'orderedList[0] is apple');
    assert.equal(orderedList[1], 'kiwi', 'orderedList[1] is kiwi');
    assert.equal(orderedList[2], 'banana', 'orderedList[2] is banana');
    assert.equal(orderedList[3], 'orange', 'orderedList[3] is orange');
    assert.equal(orderedList[4], 'potato', 'orderedList[4] is potato');
    assert.equal(orderedList[5], 'melon', 'orderedList[5] is melon');
    assert.equal(orderedList[6], 'lichi', 'orderedList[6] is lichi');
  });
}(Misago.prototype));
