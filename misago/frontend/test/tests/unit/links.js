(function () {
  'use strict';

  var service = getMisagoService('links');

  QUnit.module("Links");

  QUnit.test("staticUrl and mediaUrl", function(assert) {
    var container = {
      context: {
        'STATIC_URL': '/static/',
        'MEDIA_URL': 'http://nocookie.somewhere.com/'
      }
    };

    service(container);

    assert.equal(container.staticUrl('logo.png'), '/static/logo.png',
      'staticUrl correctly prefixed url to static asset.');
    assert.equal(
      container.mediaUrl('avatar_1.png'),
      'http://nocookie.somewhere.com/avatar_1.png',
      'mediaUrl correctly prefixed url to media asset.');
  });
}());
