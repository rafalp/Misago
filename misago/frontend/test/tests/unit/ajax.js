(function () {
  'use strict';

  QUnit.module("Ajax", {
    afterEach: function() {
      $.mockjax.clear();
    }
  });

  QUnit.test("service factory", function(assert) {
    var container = {context: {CSRF_COOKIE_NAME: 'doesnt-matter'}};

    var service = getMisagoService('ajax');
    var ajax = service(container);

    assert.ok(ajax,
      "service factory has returned service instance.");
  });

  QUnit.test("ajax success", function(assert) {
    $.mockjax({
      url: '/working-url/',
      status: 200,
      responseText: {
        'detail': 'ok'
      }
    });

    var container = { context: { CSRF_COOKIE_NAME: 'doesnt-matter' } };

    var service = getMisagoService('ajax');
    var ajax = service(container);

    var done = assert.async();

    ajax.ajax('GET', '/working-url/').then(function(data) {
      assert.equal(data.detail, 'ok', 'ajax succeeded on /working-url/');
      done();
    });
  });

  QUnit.test("ajax fail", function(assert) {
    $.mockjax({
      url: '/failing-url/',
      status: 400,
      responseText: {
        'detail': 'fail'
      }
    });

    var container = { context: { CSRF_COOKIE_NAME: 'doesnt-matter' } };

    var service = getMisagoService('ajax');
    var ajax = service(container);

    var done = assert.async();

    ajax.ajax('GET', '/failing-url/').then(function() {
      assert.ok(false, 'ajax succeeded on /failing-url/');
    }, function(rejection) {
      assert.equal(rejection.detail, 'fail',
        'ajax handled error from /failing-url/');
      done();
    });
  });

  QUnit.test("get", function(assert) {
    $.mockjax({
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'backend'
      }
    });

    var container = {
      context: {
        CSRF_COOKIE_NAME: 'doesnt-matter',
        '/test-url/': {
          'detail': 'preloaded'
        }
      }
    };

    var service = getMisagoService('ajax');
    var ajax = service(container);

    var done = assert.async();

    ajax.get('/test-url/').then(function(data) {
      assert.equal(data.detail, 'preloaded', 'get() read preloaded data');

      ajax.get('/test-url/').then(function(data) {
        assert.equal(data.detail, 'backend', 'get() read backend data');
        done();
      });
    });
  });
}());
