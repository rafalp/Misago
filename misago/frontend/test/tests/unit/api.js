(function () {
  'use strict';

  var service = getMisagoService('api');
  var container = {
      setup: {
        api: '/test-api/'
      }
    };

  QUnit.module("API");

  QUnit.test("service factory", function(assert) {
    var api = service({});
    assert.ok(api, "service factory has returned service instance.");
  });

  QUnit.test("model", function(assert) {
    var api = service(container);

    assert.equal(api.model('user', 'admin').url, '/test-api/users/admin/',
      "model constructed valid url with string pk.");

    assert.equal(api.model('user', 123).url, '/test-api/users/123/',
      "model constructed valid url with integer pk.");

    assert.equal(
      api.model('user', {token: 'abc&df', uid: 123}).url,
      '/test-api/users/?token=abc%26df&uid=123',
      "model constructed valid url with querystring.");

    assert.equal(api.model('user', 123).related('follows', 1).url,
      '/test-api/users/123/follows/1/',
      "model constructed valid related url.");

    assert.equal(api.model('user', 123).endpoint('avatar').url,
      '/test-api/users/123/avatar/',
      "model constructed valid endpoint url.");

    assert.ok(
      !api.model('user', 123).endpoint('avatar').related,
      "model can't have relation to endpoint.");

    assert.ok(
      !api.model('user', 123).related('avatar').related,
      "model can't have relation to relation.");
  });

  QUnit.test("endpoint", function(assert) {
    var api = service(container);

    assert.equal(api.endpoint('auth').url, '/test-api/auth/',
      "endpoint constructed valid url.");

    assert.equal(
      api.endpoint('auth', 'string-pk').url,
      '/test-api/auth/string-pk/',
      "endpoint constructed valid url with string pk.");

    assert.equal(
      api.endpoint('auth', 124).url,
      '/test-api/auth/124/',
      "endpoint constructed valid url with integer pk.");

    assert.equal(
      api.endpoint('auth', {token: 'abc&df', uid: 123}).url,
      '/test-api/auth/?token=abc%26df&uid=123',
      "endpoint constructed valid url with querystring.");

    assert.ok(
      !api.endpoint('auth', 124).related,
      "endpoint can't have nested relation.");

    assert.equal(
      api.endpoint('auth', 124).endpoint('change-password').url,
      '/test-api/auth/124/change-password/',
      "nested endpoint constructed valid url with integer pk.");

    assert.ok(
      !api.endpoint('auth', 124).endpoint('change-password').endpoint,
      "nested endpoint can't be nested further.");
  });
}());
