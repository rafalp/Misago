(function () {
  'use strict';

  var app = null;

  QUnit.acceptance("Request Activation Link", {
    beforeEach: function() {
      app = initTestMisago();
    },
    afterEach: function() {
      app.destroy();
    }
  });

  QUnit.test('with empty input', function(assert) {
    app.router.route('/activation/');

    var done = assert.async();

    click('.well-form .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Enter a valid email address.",
        "request form raised alert about empty input.");
      done();
    });
  });

  QUnit.test('with invalid email', function(assert) {
    app.router.route('/activation/');

    var done = assert.async();

    fillIn('.well-form input', 'not-email');
    click('.well-form .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), "Enter a valid email address.",
        "request form raised alert about empty input.");
      done();
    });
  });

  QUnit.test('with backend banned', function(assert) {
    $.mockjax({
      url: '/test-api/auth/send-activation/',
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

    app.router.route('/activation/');

    var done = assert.async();

    fillIn('.well-form input', 'valid@email.com');
    click('.well-form .btn-primary');

    onElement('.page-error.page-error-banned .message-body', function() {
      assert.ok(true, "Permission denied error page was displayed.");
      assert.equal(
        getElementText('.page .message-body .lead'),
        "This is test ban.",
        "Banned page displayed ban message.");
      done();
    });
  });

  QUnit.test('with backend error', function(assert) {
    var message = "No user found for email!";
    $.mockjax({
      url: '/test-api/auth/send-activation/',
      status: 400,
      responseText: {
        'detail': message
      }
    });

    app.router.route('/activation/');

    var done = assert.async();

    fillIn('.well-form input', 'valid@email.com');
    click('.well-form .btn-primary');

    onElement('.alerts .alert-danger', function() {
      assert.equal(getAlertMessage(), message,
        "request form raised alert returned by backend.");
      done();
    });
  });

  QUnit.test('with success', function(assert) {
    $.mockjax({
      url: '/test-api/auth/send-activation/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    app.router.route('/activation/');

    var done = assert.async();

    fillIn('.well-form input', 'valid@email.com');
    click('.well-form .btn-primary');

    onElement('.message-body p', function() {
      assert.equal(
        getElementText('.message-body p:nth-child(2)'),
        "Bob, we have sent your activation link to bob@boberson.com.",
        "request form displayed success message.");
      done();
    });
  });

  QUnit.test('reset', function(assert) {
    $.mockjax({
      url: '/test-api/auth/send-activation/',
      status: 200,
      responseText: {
        'username': 'Bob',
        'email': 'bob@boberson.com'
      }
    });

    app.router.route('/activation/');

    var done = assert.async();

    fillIn('.well-form input', 'valid@email.com');
    click('.well-form .btn-primary');
    waitForElement('.message-body .btn-default');
    click('.message-body .btn-default');

    onElement('.well-form', function() {
      assert.ok(true, 'reset button took client back to previous screen.');
      done();
    });
  });
}());
