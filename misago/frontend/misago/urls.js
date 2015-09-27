(function (Misago, UrlConf) {
  'use strict';

  var urls = new UrlConf();
  urls.url('/', Misago.IndexRoute, 'index');

  // Legal pages
  urls.url(
    '/terms-of-service/',
    Misago.TermsOfServiceRoute,
    'terms_of_service');

  urls.url(
    '/privacy-policy/',
    Misago.PrivacyPolicyRoute,
    'privacy_policy');

  // Catch-all 404 not found route
  urls.url('/:rest...', Misago.Error404Route, 'not_found');

  Misago.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
