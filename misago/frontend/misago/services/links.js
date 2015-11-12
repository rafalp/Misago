(function (Misago) {
  'use strict';

  var setLinks = function(_) {
    _.baseUrl = $('base').attr('href');

    var staticUrl = Misago.get(_.context, 'STATIC_URL', '/');
    var mediaUrl = Misago.get(_.context, 'MEDIA_URL', '/');

    // Media/Static urls
    var prefixUrl = function(prefix) {
      return function(url) {
        return prefix + url;
      };
    };

    _.staticUrl = prefixUrl(staticUrl);
    _.mediaUrl = prefixUrl(mediaUrl);
  };

  Misago.addService('links', function(_) {
    setLinks(_);
  });
}(Misago.prototype));
