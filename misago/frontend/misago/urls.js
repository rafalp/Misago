(function (Misago, UrlConf) {
  'use strict';

  var urls = new UrlConf();
  urls.url('/', 'index');

  // Legal pages
  urls.url(
    '/terms-of-service/',
    'terms_of_service');

  urls.url(
    '/privacy-policy/',
    'privacy_policy');

  // Catch-all 404 not found route
  urls.url('/:rest...', 'error:404', 'not_found');

  Misago.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
