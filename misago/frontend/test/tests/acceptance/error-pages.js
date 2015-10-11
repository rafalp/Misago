(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Error Pages", {
    beforeEach: function() {
      app = initTestMisago();
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test("Error banned", function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      status: 403,
      responseText: {
        'detail': 'You are banned!',
        'ban': {
          'expires_on': null,
          'message': {
            'plain': 'This is test ban.',
            'html': '<p>This is test ban.</p>'
          }
        }
      }
    });

    var done = assert.async();

    click('.footer-nav li:first-child a');
    onElement('.page-error.page-error-banned .error-message', function() {
      assert.ok(true, "Permission denied error page was displayed.");
      assert.equal(
        getElementText('.page .error-message .lead'),
        "This is test ban.",
        "Banned page displayed ban message.");
      done();
    });
  });

  QUnit.test("Error 403 with message", function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      status: 403,
      responseText: {
        'detail': "I can't let you do this Dave."
      }
    });

    var done = assert.async();

    click('.footer-nav li:first-child a');
    onElement('.page-error.page-error-403 .error-message', function() {
      assert.ok(true, "Permission denied error page was displayed.");
      assert.equal(
        getElementText('.page .error-message .help'),
        "I can't let you do this Dave.",
        "Permission denied error page used backend message.");
      done();
    });
  });

  QUnit.test("Error 403 without message", function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      status: 403,
      responseText: {
        'detail': 'Permission denied'
      }
    });

    var done = assert.async();

    click('.footer-nav li:first-child a');
    onElement('.page-error.page-error-403 .error-message', function() {
      assert.ok(true, "Permission denied error page was displayed.");
      assert.equal(
        getElementText('.page .error-message .help'),
        "You don't have permission to access this page.",
        "Permission denied error page used default message.");
      done();
    });
  });

  QUnit.test("Error 404", function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      status: 404
    });

    var done = assert.async();

    click('.footer-nav li:first-child a');
    onElement('.page-error.page-error-404', function() {
      assert.ok(true, "Not found error page was displayed.");
      done();
    });
  });

  QUnit.test("Error 404 on invalid url", function(assert) {
    var done = assert.async();
    m.route('/some-invalid-url-is-her!');
    onElement('.page-error.page-error-404', function() {
      assert.ok(true, "Not found error page was displayed.");
      done();
    });
  });

  QUnit.test("Error 500", function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      status: 500
    });

    var done = assert.async();

    click('.footer-nav li:first-child a');
    onElement('.page-error.page-error-500', function() {
      assert.ok(true, "Backend error page was displayed.");
      done();
    });
  });

  QUnit.test("Error 0", function(assert) {
    $.mockjax({
      url: '/test-api/legal-pages/terms-of-service/',
      isTimeout: true
    });

    var done = assert.async();

    click('.footer-nav li:first-child a');
    onElement('.page-error.page-error-0', function() {
      assert.ok(true, "Timeout error page was displayed.");
      done();
    });
  });
}());
