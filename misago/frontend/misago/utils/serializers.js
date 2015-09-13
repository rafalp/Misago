(function (Misago) {
  Misago.deserializeDatetime = function(deserialized) {
    return deserialized ? moment(deserialized) : null;
  };

  Misago.serializeDatetime = function(serialized) {
    return serialized ? serialized.format() : null;
  };
} (Misago.prototype));
