(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Auth Exceptions", {
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test("denyAuthenticated denied authenticated", function(assert) {
    app = initTestMisago({
      user: mockUser()
    });

    var done = assert.async();

    app.router.route('/activation/');

    onElement('.page-error.page-error-403 .message-body', function() {
      assert.ok(true, "Permission denied error page was displayed.");
      assert.equal(
        getElementText('.page .message-body p:last-child'),
        "You have to be signed out to activate account.",
        "Route access was denied with valid error.");
      done();
    });
  });

  QUnit.test("denyAuthenticated passed anonymous", function(assert) {
    app = initTestMisago();

    var done = assert.async();

    app.router.route('/activation/');

    onElement('.page-request-activation', function() {
      assert.ok(true, "Access to route was granted for anonymous user.");
      done();
    });
  });
}());
