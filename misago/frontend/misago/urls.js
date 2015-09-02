(function (Misago, UrlConf) {
  'use strict';

  var urls = new UrlConf();
  urls.url('/', Misago.IndexPage, 'index');

  // Legal pages
  urls.url('/terms-of-service/', Misago.TermsOfServicePage, 'terms_of_service');
  urls.url('/privacy-policy/', Misago.PrivacyPolicyPage, 'privacy_policy');

  Misago.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
