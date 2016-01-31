import assert from 'assert';
import { Ajax } from 'misago/services/ajax';

var ajax = null;

describe('Ajax', function() {
  beforeEach(function() {
    document.cookie = '';

    ajax = new Ajax();
    ajax.init('csrf_token');
  });

  afterEach(function() {
    document.cookie = '';
    $.mockjax.clear();
  });

  it("handles csrf token", function() {
    ajax = new Ajax();
    ajax.init('csrf_token');

    assert.strictEqual(ajax.getCsrfToken(), null,
      "function returned null for unset cookie");

    document.cookie = 'csrf_token=t3stt0k3n';
    assert.equal(ajax.getCsrfToken(), 't3stt0k3n', "set cookie was returned");

    ajax = new Ajax();
    ajax.init('csrf_token');

    assert.equal(ajax._csrfToken, 't3stt0k3n',
      "csrf token was read and set on init");
  });

  it("resolves request to backend", function(done) {
    $.mockjax({
      url: '/working-url/',
      status: 200,
      dataType: 'json',
      responseText: {
        'detail': 'ok'
      }
    });

    ajax.request('GET', '/working-url/').then(function(data) {
      assert.equal(data.detail, 'ok', "ajax succeeded on /working-url/");
      done();
    });
  });

  it("rejects request to backend", function(done) {
    $.mockjax({
      url: '/failing-url/',
      status: 400,
      responseText: {
        'detail': 'fail'
      }
    });

    ajax.request('GET', '/failing-url/').then(function() {
      assert.fail("request to /failing-url/ should be rejected");
    }, function(rejection) {
      assert.equal(rejection.detail, 'fail',
        "ajax handled error from /failing-url/");
      done();
    });
  });

  it("normalizes disconnection error", function(done) {
    $.mockjax({
      url: '/failing-url/',
      isTimeout: true
    });

    ajax.request('GET', '/failing-url/').then(function() {
      assert.fail("request to /failing-url/ should be rejected");
    }, function(rejection) {
      assert.equal(rejection.status, 0, "rejection status code is preserved");
      assert.equal(rejection.detail, "Lost connection with application.",
        "ajax handled disconnection from /failing-url/");
      done();
    });
  });

  it("makes GET request", function(done) {
    $.mockjax({
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'ok'
      }
    });

    ajax.get('/test-url/').then(function(data) {
      assert.equal(data.detail, 'ok', "GET succeeded");
      done();
    });
  });

  it("makes GET request with querystring", function(done) {
    $.mockjax({
      url: '/test-url/?user=123&text=lorem',
      status: 200,
      responseText: {
        'detail': 'ok'
      }
    });

    ajax.get('/test-url/', {user: 123, text: 'lorem'}).then(function(data) {
      assert.equal(data.detail, 'ok', "GET with querystring succeeded");
      done();
    });
  });

  it("makes PATCH request", function(done) {
    $.mockjax({
      type: 'PATCH',
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'patched'
      }
    });

    ajax.patch('/test-url/').then(function(data) {
      assert.equal(data.detail, 'patched', "PATCH succeeded");
      done();
    });
  });

  it("makes PUT request", function(done) {
    $.mockjax({
      type: 'PUT',
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'put'
      }
    });

    ajax.put('/test-url/').then(function(data) {
      assert.equal(data.detail, 'put', "PUT succeeded");
      done();
    });
  });

  it("makes DELETE request", function(done) {
    $.mockjax({
      type: 'DELETE',
      url: '/test-url/',
      status: 200,
      responseText: {
        'detail': 'deleted'
      }
    });

    ajax.delete('/test-url/').then(function(data) {
      assert.equal(data.detail, 'deleted', "DELETE succeeded");
      done();
    });
  });
});
