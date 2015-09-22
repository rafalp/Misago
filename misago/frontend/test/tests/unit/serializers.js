(function (Misago) {
  'use strict';

  QUnit.module("Serializers");

  QUnit.test("datetime", function(assert) {
    assert.equal(Misago.serializeDatetime(null), null,
      "serialization of null datetime value returned null");
    assert.equal(Misago.deserializeDatetime(null), null,
      "deserialization of null datetime value returned null");

    var test_moment = moment();

    assert.equal(
      Misago.serializeDatetime(test_moment), test_moment.format(),
      "datetime was serialized to string");

    assert.equal(
      Misago.deserializeDatetime(test_moment.format()).format(),
      test_moment.format(),
      "datetime was deserialized to momentjs object");
  });
}(Misago.prototype));
