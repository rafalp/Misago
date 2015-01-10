// Just an container for Misago js
// ===============================
var Misago = {}

Misago.getattr = function(obj, path) {
  if (obj == undefined) {
    return undefined;
  }

  $.each(path.split("."), function(i, bit) {
    obj = obj[bit];
  })
  return obj;
}
