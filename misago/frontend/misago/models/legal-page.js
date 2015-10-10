(function (Misago) {
  'use strict';

  var LegalPage = function(data) {
    this.title = data.title;
    this.body = data.body;
    this.link = data.link;
  };

  Misago.addService('model:legal-page', function(_) {
    _.models.add('legal-page', {
      class: LegalPage
    });
  },
  {
    after: 'models'
  });
} (Misago.prototype));
