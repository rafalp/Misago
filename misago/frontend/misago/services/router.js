(function (ns) {
  'use strict';

  var prefixUrl = function(prefix) {
    return function(url) {
      return prefix + url;
    };
  };

  var Router = function(_) {
    this.base_url = $('base').attr('href');

    this.url = function() {
      return '/';
    };

    // Media/Static url functions
    this.staticUrl = prefixUrl(_.get(_.preloaded_data, 'STATIC_URL', '/'));
    this.mediaUrl = prefixUrl(_.get(_.preloaded_data, 'MEDIA_URL', '/'));
  };

  ns.RouterFactory = function(_) {
    return new Router(_);
  };
}(Misago.prototype));
