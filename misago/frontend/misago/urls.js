(function (Misago, UrlConf) {
  'use strict';

  var urls = new UrlConf();

  // Board index
  urls.url('/', 'index');

  // Account activation
  urls.url('/activation/', 'request_activation');
  urls.url('/activation/:user_id/:token/', 'activate_by_token');

  // Legal pages
  urls.url('/terms-of-service/', 'terms_of_service');
  urls.url('/privacy-policy/', 'privacy_policy');

  // Catch-all 404 not found route
  urls.url('/:rest...', 'error:404', 'not_found');

  Misago.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
