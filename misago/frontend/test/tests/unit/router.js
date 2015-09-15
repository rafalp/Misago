(function () {
  'use strict';

  QUnit.module("Router");

  QUnit.test("cleanUrl cleans url's that should be routed", function(assert) {
    var container = {
      context: {
        'STATIC_URL': '/static/',
        'MEDIA_URL': 'http://nocookie.somewhere.com/'
      }
    };

    var service = getMisagoService('router');
    var router = service(container);

    assert.equal(router.cleanUrl('/'), '/');
    assert.equal(router.cleanUrl('/lorem-ipsum/'), '/lorem-ipsum/');
    assert.equal(router.cleanUrl('/lorem-ipsum/dolor/'), '/lorem-ipsum/dolor/');

    assert.equal(router.cleanUrl('/static/'), undefined);
    assert.equal(router.cleanUrl('http://nocookie.somewhere.com/'), undefined);
    assert.equal(router.cleanUrl('/static/test.png'), undefined);
    assert.equal(router.cleanUrl('http://nocookie.somewhere.com/test.png'), undefined);

    container.context.STATIC_URL = '/misago/static/';
    router = service(container);
    router.baseUrl = '/misago/';

    assert.equal(router.cleanUrl('/misago/'), '/misago/');
    assert.equal(router.cleanUrl('/misago/lorem-ipsum/'), '/misago/lorem-ipsum/');
    assert.equal(router.cleanUrl('/misago/lorem-ipsum/dolor/'), '/misago/lorem-ipsum/dolor/');

    assert.equal(router.cleanUrl('/'), undefined);
    assert.equal(router.cleanUrl('/lorem-ipsum/'), undefined);
    assert.equal(router.cleanUrl('/lorem-ipsum/dolor/'), undefined);

    assert.equal(router.cleanUrl('/misago/static/'), undefined);
    assert.equal(router.cleanUrl('http://nocookie.somewhere.com/'), undefined);
    assert.equal(router.cleanUrl('/misago/static/test.png'), undefined);
    assert.equal(router.cleanUrl('http://nocookie.somewhere.com/test.png'), undefined);
  });

  QUnit.test("staticUrl and mediaUrl prefix paths", function(assert) {
    var container = {
      context: {
        'STATIC_URL': '/static/',
        'MEDIA_URL': 'http://nocookie.somewhere.com/'
      }
    };

    var service = getMisagoService('router');
    var router = service(container);

    assert.equal(router.staticUrl('logo.png'), '/static/logo.png', 'staticUrl correctly prefixed url to static asset.');
    assert.equal(router.mediaUrl('avatar_1.png'), 'http://nocookie.somewhere.com/avatar_1.png', 'mediaUrl correctly prefixed url to media asset.');
  });
}());
