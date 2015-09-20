(function (Misago) {
  Misago.serializeDatetime = function(serialized) {
    return serialized ? serialized.format() : null;
  };

  Misago.deserializeDatetime = function(deserialized) {
    return deserialized ? moment(deserialized) : null;
  };
}(Misago.prototype));
