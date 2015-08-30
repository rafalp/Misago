(function (ns, UrlConf) {
  'use strict';

  var urls = new UrlConf();
  urls.url('/', ns.IndexPage, 'index');

  // Legal pages
  urls.url('/terms-of-service/', ns.TermsOfServicePage, 'terms_of_service');
  urls.url('/privacy-policy/', ns.PrivacyPolicyPage, 'privacy_policy');

  ns.urls = urls;
} (Misago.prototype, Misago.prototype.UrlConf));
