(function (Misago) {
  'use strict';

  var LegalPage = function(data) {
    this.title = data.title;
    this.body = data.body;
  };

  Misago.addService('legal-page-model', function(_) {
    _.models.add('legal-page', {
      class: LegalPage
    });
  }, {after: 'models'});
} (Misago.prototype));
