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

  Misago.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
