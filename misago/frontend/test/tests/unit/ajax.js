(function () {
  'use strict';

  QUnit.module("Ajax", {
    afterEach: function() {
      $.mockjax.clear();
    }
  });

  QUnit.test("service factory", function(assert) {
    var container = {
      context: {
        CSRF_COOKIE_NAME: 'doesnt-matter'
      }
    };

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

    var container = {
      context: {
        CSRF_COOKIE_NAME: 'doesnt-matter'
      }
    };

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

    var container = {
      context: {
        CSRF_COOKIE_NAME: 'doesnt-matter'
      }
    };

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
        CSRF_COOKIE_NAME: 'doesnt-matter'
      }
    };

    var service = getMisagoService('ajax');
    var ajax = service(container);

    var done = assert.async();

    ajax.get('/test-url/').then(function(data) {
      assert.equal(data.detail, 'backend', 'get() read backend data');
      done();
    });
  });

  QUnit.test("post, patch, put, delete", function(assert) {
    $.mockjax({
      type: 'POST',
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'posted'
      }
    });

    $.mockjax({
      type: 'PATCH',
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'patched'
      }
    });

    $.mockjax({
      type: 'PUT',
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'put'
      }
    });

    $.mockjax({
      type: 'DELETE',
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'deleted'
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

    var donePost = assert.async();
    var donePatch = assert.async();
    var donePut = assert.async();
    var doneDelete = assert.async();

    ajax.post('/test-url/', {}).then(function(data) {
      assert.equal(data.detail, 'posted', 'post() call succeeded');
      donePost();
    });

    ajax.patch('/test-url/', {}).then(function(data) {
      assert.equal(data.detail, 'patched', 'patch() call succeeded');
      donePatch();
    });

    ajax.put('/test-url/', {}).then(function(data) {
      assert.equal(data.detail, 'put', 'put() call succeeded');
      donePut();
    });

    ajax.delete('/test-url/').then(function(data) {
      assert.equal(data.detail, 'deleted', 'delete() call succeeded');
      doneDelete();
    });
  });

  QUnit.test("alert", function(assert) {
    var unknownError = assert.async();
    var disconnectedError = assert.async();
    var deniedError = assert.async();
    var notFoundError = assert.async();

    var container = {
      context: {
        CSRF_COOKIE_NAME: 'doesnt-matter'
      },
      setup: {
        api: '/test-api/'
      },
      alert: {
        error: function(message) {
          if (message === "Unknown error has occured.") {
            assert.ok(true, "unknown error was handled.");
            unknownError();
          }

          if (message === "Lost connection with application.") {
            assert.ok(true, "error 0 was handled.");
            disconnectedError();
          }

          if (message === "You don't have permission to perform this action.") {
            assert.ok(true, "error 403 was handled.");
            deniedError();
          }

          if (message === "Action link is invalid.") {
            assert.ok(true, "error 404 was handled.");
            notFoundError();
          }
        }
      }
    };

    var service = getMisagoService('ajax');
    var ajax = service(container);

    ajax.alert({
      status: 500
    });
    ajax.alert({
      status: 0
    });
    ajax.alert({
      status: 403,
      detail: "Permission denied"
    });
    ajax.alert({
      status: 404,
      detail: "Not found"
    });
  });
}());
